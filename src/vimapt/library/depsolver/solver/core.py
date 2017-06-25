import six

import collections

from ..errors \
    import \
        DepSolverError

from ..compat \
    import \
        OrderedDict
from ..bundled.traitlets \
    import \
        HasTraits, Instance, List, Long

from ..solver.decisions \
    import \
        DecisionsSet
from ..solver.operations \
    import \
        Install, Update
from ..pool \
    import \
        Pool
from ..repository \
    import \
        Repository
from ..request \
    import \
        Request
from .policy \
    import \
        DefaultPolicy
from .rules_generator \
    import \
        RulesGenerator, RulesSet
from .rules_watch_graph \
    import \
        RulesWatchGraph, RuleWatchNode
from .transaction \
    import \
        Transaction

_BRANCH_INFO = collections.namedtuple("_BranchInfo", ["literals", "level"])

# FIXME: the php model for this class is pretty broken as many attributes are
# initialized outside the ctor. Fix this.
class Solver(HasTraits):
    policy = Instance(DefaultPolicy)
    pool = Instance(Pool)
    installed_repository = Instance(Repository)

    installed_map = Instance(OrderedDict)
    update_map = Instance(OrderedDict)

    _propagate_index = Long(-1)
    _learnt_why = Instance(OrderedDict)
    _branches = List(Instance(_BRANCH_INFO))

    def __init__(self, pool, installed_repository, **kw):
        policy = DefaultPolicy()
        installed_map = OrderedDict()
        update_map = OrderedDict()
        learnt_why = OrderedDict()
        branches = []
        super(Solver, self).__init__(self, policy=policy, pool=pool,
                installed_repository=installed_repository,
                installed_map=installed_map,
                update_map=update_map,
                _learnt_why=learnt_why,
                _branches=branches, **kw)

    def solve(self, request):
        decisions = self._solve(request)
        return self._calculate_transaction(decisions)

    def _solve(self, request):
        decisions, rules_set = self._prepare_solver(request)
        self._make_assertion_rules_decisions(decisions, rules_set)

        watch_graph = RulesWatchGraph()
        for rule in rules_set:
            watch_graph.insert(RuleWatchNode(rule))
        self._run_sat(decisions, rules_set, watch_graph, True)

        for package_id in self.installed_map:
            if decisions.is_undecided(package_id):
                decisions.decide(-package_id, 1, "")

        return decisions

    def _calculate_transaction(self, decisions):
        transaction = Transaction(self.pool, self.policy, self.installed_map, decisions)
        return transaction.compute_operations()

    def _setup_install_map(self, jobs):
        for package in self.installed_repository.iter_packages():
            self.installed_map[package.id] = package

        for job in jobs:
            if job.job_type == "update":
                for package in job.packages:
                    if package.id in self.installed_map:
                        self.update_map[package.id] = True
            elif job.job_type == "upgrade":
                for package_id in self.installed_map:
                    self.update_map[package_id] = True
            elif job.job_type == "install":
                if len(job.packages) < 1:
                    raise NotImplementedError()

    def _prepare_solver(self, request):
        self._setup_install_map(request.jobs)

        decisions = DecisionsSet(self.pool)

        rules_generator = RulesGenerator(self.pool, request, self.installed_map)
        return decisions, rules_generator.iter_rules()

    def _make_assertion_rules_decisions(self, decisions, rules_generator):
        decision_start = len(decisions) - 1

        for rule in rules_generator:
            if not rule.is_assertion or not rule.enabled:
                continue

            literals = rule.literals
            literal = literals[0]

            if not decisions.is_decided(abs(literal)):
                decisions.decide(literal, 1, rule)
                continue;

            if decisions.satisfy(literal):
                continue

            if rule.rule_type == "learnt":
                rule.enable = False
                continue

            raise NotImplementedError()

    def _propagate(self, decisions, watch_graph, level):
        while decisions.is_offset_valid(self._propagate_index):
            decision = decisions.at_offset(self._propagate_index)

            conflict = watch_graph.propagate_literal(
                    decision.literal, level, decisions)

            self._propagate_index += 1
            if conflict is not None:
                return conflict

        return None

    def _prune_updated_packages(self, decision_queue):
        # prune all update packages until installed version except for
        # requested updates
        if len(self.installed_repository) != len(self.update_map):
            pruned_queue = []
            for literal in decision_queue:
                package_id = abs(literal)
                if package_id in self.installed_map:
                    pruned_queue.append(literal)
                    if package_id in self.update_map:
                        pruned_queue = decision_queue
                        break
            decision_queue = pruned_queue
        return decision_queue

    def _set_propagate_learn(self, decisions, rules_set, watch_graph, level, literal, disable_rules, rule):
        """
        add free decision (a positive literal) to decision queue
        increase level and propagate decision
        return if no conflict.

        in conflict case, analyze conflict rule, add resulting
        rule to learnt rule set, make decision from learnt
        rule (always unit) and re-propagate.

        returns the new solver level or 0 if unsolvable
        """
        level += 1

        decisions.decide(literal, level, rule)

        while True:
            rule = self._propagate(decisions, watch_graph, level)
            if rule is None:
                break

            if level == 1:
                raise NotImplementedError()
                #return $this->analyzeUnsolvable($rule, $disableRules);

            # conflict
            learn_literal, new_level, new_rule, why = self._analyze(level, rule)

            if new_level <= 0 or new_level >= level:
                raise DepSolverError(
                    "Trying to revert to invalid level %s from level %s" % (new_level, level)
                )
            elif new_rule is None:
                raise DepSolverError(
                    "No rule was learned from analyzing %s at level %d." % (rule, level)
                )

            level = new_level
            self._revert(level)

            rules_set.add_rule(new_ruile, "learnt")
            self._learnt_why[new_rule.id] = why

            rule_node = RuleWatchNode(new_ule)
            rule_node.watch2_on_highest(decisions)
            watch_graph.insert(rule_node)

            decisions.decide(learn_literal, level, new_rule)
        return level

    def _select_and_install(self, decisions, rules_set, watch_graph, level, decision_queue, disable_rules, rule):
        literals = self.policy.select_preferred_packages(self.pool,
                self.installed_map, decision_queue)

        if len(literals) == 0:
            raise DepSolverError("Internal error in solver.")
        else:
            selected_literal, literals = literals[0], literals[1:]
            if len(literals) > 0:
                self._branches.append((literals, level))

            return self._set_propagate_learn(decisions, rules_set, watch_graph,
                    level, selected_literal, disable_rules, rule)


    def _run_sat(self, decisions, rules_set, watch_graph, disable_rules=True):
        self._propagate_index = 0

        # here's the main loop:
        # 1) propagate new decisions (only needed once)
        # 2) fulfill jobs
        # 3) fulfill all unresolved rules
        # 4) minimalize solution if we had choices
        # if we encounter a problem, we rewind to a safe level and restart
        # with step 1

        decision_queue = []
        decision_supplement_queue = []
        disable_rules = []

        level = 1
        system_level = level + 1
        installed_pos = 0

        while True:
            if level == 1:
                conflict_rule = self._propagate(decisions, watch_graph, level)
                if conflict_rule is not None:
                    raise NotImplementedError("analyzing conflict rules not yet implemented")

            # Handle job rules
            if level < system_level:
                for rule in rules_set.job_rules:
                    if rule.enabled:
                        decision_queue = []
                        none_satisfied = True

                        for literal in rule.literals:
                            if decisions.satisfy(literal):
                                none_satisfied = False
                                break

                            if literal > 0 and decisions.is_undecided(literal):
                                decision_queue.append(literal)

                        if none_satisfied and len(decision_queue) > 0:
                            decision_queue = self._prune_updated_packages(decision_queue)

                        if none_satisfied and len(decision_queue) > 0:
                            old_level = level
                            level = self._select_and_install(decisions,
                                    rules_set, watch_graph, level, decision_queue,
                                    disable_rules, rule)

                            if level == 0:
                                return
                            if level <= old_level:
                                break
                system_level = level + 1

            if level < system_level:
                system_level = level

            rule_id = 0
            n = 0
            while n < len(rules_set):
                if rule_id == len(rules_set):
                    rule_id = 0

                rule = rules_set.rules_by_id[rule_id]
                rule_id += 1
                n += 1

                if not rule.enabled:
                    continue

                decision_queue = []

                if _is_rule_fulfilled(rule, decisions, decision_queue):
                    continue

                # need to have at least 2 item to pick from
                if len(decision_queue) < 2:
                    continue

                o_level = level
                level = self._select_and_install(decisions, rules_set, watch_graph, level, decision_queue,
                            disable_rules, rule)

                if level == 0:
                    return

                n = 0

            if level < system_level:
                continue

            break

def _is_rule_fulfilled(rule, decisions, decision_queue):
    # make sure that
    # * all negative literals are installed
    # * no positive literal is installed
    # i.e. the rule is not fulfilled and we
    # just need to decide on the positive literals
    #
    for literal in rule.literals:
        if literal <= 0:
            if not decisions.is_decided_install(abs(literal)):
                return True
        else:
            if decisions.is_decided_install(abs(literal)):
                return True
            if decisions.is_undecided(abs(literal)):
                decision_queue.append(literal)
    return False
