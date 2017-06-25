import collections

import six

from ..compat \
    import \
        OrderedDict
from ..bundled.traitlets \
    import \
        HasTraits, Dict, Enum, Instance, List, Long, Set, Unicode
from ..errors \
    import \
        MissingRequirementInPool
from ..solver.policy \
    import \
        DefaultPolicy
from ..pool \
    import \
        Pool
from ..request \
    import \
        Request
from ..requirement \
    import \
        Requirement
from .rule \
    import \
        PackageRule

R = Requirement.from_string

class RulesSet(HasTraits):
    """
    Simple container of rules
    """
    unknown_rules = List(Instance(PackageRule))
    package_rules = List(Instance(PackageRule))
    job_rules = List(Instance(PackageRule))
    learnt_rules = List(Instance(PackageRule))

    rule_types = Enum(["unknown", "package", "job", "learnt"])

    rules_by_hash = Dict()
    rules_by_id = List(Instance(PackageRule))

    def __init__(self, **kw):
        super(RulesSet, self).__init__(**kw)

    def __len__(self):
        return len(self.rules_by_id)

    def __contains__(self, rule):
        # FIXME: implementing bucketing is a bit insane. To be removed once
        # direct porting of composer is finished.
        if rule.rule_hash in self.rules_by_hash:
            candidates = self.rules_by_hash[rule.rule_hash]
            for candidate in candidates:
                if rule.is_equivalent(candidate):
                    return True
            return False
        else:
            return False

    def __iter__(self):
        return iter(self.rules_by_id)

    def add_rule(self, rule, rule_type):
        if rule_type == "unknown":
            self.unknown_rules.append(rule)
        elif rule_type == "package":
            self.package_rules.append(rule)
        elif rule_type == "job":
            self.job_rules.append(rule)
        elif rule_type == "learnt":
            self.learnt_rules.append(rule)
        else:
            raise DepSolverError("Invalid rule_type %s" % (rule_type,))

        rule.id = len(self.rules_by_id)
        rule.type = rule_type
        self.rules_by_id.append(rule)

        rules = self.rules_by_hash.get(rule.rule_hash, [])
        rules.append(rule)
        self.rules_by_hash[rule.rule_hash] = rules

class RulesGenerator(HasTraits):
    pool = Instance(Pool)
    rules_set = Instance(RulesSet)

    policy = Instance(DefaultPolicy)
    request = Instance(Request)

    installed_map = Instance(OrderedDict)
    added_package_ids = Set()

    def __init__(self, pool, request, installed_map, policy=None, **kw):
        if policy is None:
            policy = DefaultPolicy()

        rules_set = RulesSet()
        added_package_ids = set()
        super(RulesGenerator, self).__init__(pool=pool, request=request,
                installed_map=installed_map, policy=policy,
                rules_set=rules_set, added_package_ids=added_package_ids, **kw)

    def iter_rules(self):
        """
        Return an iterator over each created rule.
        """
        jobs = self.request.jobs

        #print "start", self.installed_map
        for package in six.itervalues(self.installed_map):
            #print "@"
            self._add_package_rules(package)
            #print "@@"
            self._add_updated_packages_rules(package)
        #print "end"

        self._add_job_rules()
        return self.rules_set

    #-------------------------------
    # API to create individual rules
    #-------------------------------
    def _create_dependency_rule(self, package, dependencies, reason, reason_details=""):
        """
        Create the rule for the dependencies of a package.

        This dependency is of the form (-A | R1 | R2 | R3) where R* are the set
        of packages provided by the dependency requirement.

        Parameters
        ----------
        package: PackageInfo
            The package with a requirement
        dependencies: sequence
            Sequence of packages that fulfill the requirement.
        reason: str
            A valid PackageRule.reason value
        reason_details: str
            Optional details explaining that rule origin.

        Returns
        -------
        rule: PackageRule or None
        """
        literals = [-package.id]

        for dependency in dependencies:
            if dependency == package:
                return
            else:
                literals.append(dependency.id)

        return PackageRule(self.pool, literals, reason, reason_details, version_factory=package.version_factory)

    def _create_conflicts_rule(self, issuer, provider, reason, reason_details=""):
        """
        Create a conflict rule between issuer and provider

        The rule is of the form (-A | -B)

        Parameters
        ----------
        issuer: PackageInfo
            Package declaring the conflict
        provider: PackageInfo
            Package causing the conflict
        reason: str
            One of PackageRule.reason
        reason_details: str
            Optional details explaining that rule origin.

        Returns
        -------
        rule: PackageRule or None
        """
        if issuer != provider:
            return PackageRule(self.pool, [-issuer.id, -provider.id], reason, reason_details)

    def _create_install_one_rule(self, packages, reason, job):
        """
        Creates a rule to Install one of the given packages.

        The rule is of the form (A | B | C)

        Parameters
        ----------
        packages: sequence
            List of packages to choose from
        reason: str
            One of PackageRule.reason
        job: _Job
            The job this rule was created from

        Returns
        -------
        rule: PackageRule
        """
        literals = [p.id for p in packages]
        return PackageRule(self.pool, literals, reason, job.requirement.name, job)

    #--------------------------------------------------
    # API to assemble individual rules from requirement
    #--------------------------------------------------
    def _add_rule(self, rule, rule_type):
        """
        Add the given rule to the internal rules set.

        Does nothing if the rule is None.

        Parameters
        ----------
        rule: PackageRule or None
            The rule to add
        rule_type: str
            Rule's  type
        """
        if rule is not None and rule not in self.rules_set:
            self.rules_set.add_rule(rule, rule_type)

    def _add_package_rules(self, package):
        """
        Create all the rules required to satisfy installing the given package.
        """
        #print "add package rule", package
        work_queue = collections.deque()
        work_queue.append(package)

        while len(work_queue) > 0:
            p = work_queue.popleft()

            if not p.id in self.added_package_ids:
                self.added_package_ids.add(p.id)

                for dependency in p.dependencies:
                    dependency_candidates = self.pool.what_provides(dependency)
                    #print [p.id for p in dependency_candidates]
                    rule = self._create_dependency_rule(p,
                            dependency_candidates, "package_requires",
                            str(dependency))
                    self._add_rule(rule, "package")

                    for candidate in dependency_candidates:
                        work_queue.append(candidate)

                for conflict in p.conflicts:
                    conflict_candidates = self.pool.what_provides(conflict)

                    for conflict_candidate in conflict_candidates:
                        rule = self._create_conflicts_rule(p,
                                conflict_candidate, "package_conflict",
                                "%s conflict with %s" % (p.name, str(conflict_candidate)))
                        self._add_rule(rule, "package")

                is_installed = p.id in self.installed_map
                for replace in p.replaces:
                    replace_candidates = self.pool.what_provides(replace)

                    for replace_candidate in replace_candidates:
                        if replace_candidate != p:
                            if is_installed:
                                reason = "rule_installed_package_obsoletes"
                            else:
                                reason = "package_obsoletes"
                            rule = self._create_conflicts_rule(p,
                                    replace_candidate, reason,
                                    "%s replaces %s" % (p.name, str(replace_candidate)))
                            self._add_rule(rule, "package")

                obsolete_providers = self.pool.what_provides(R(p.name))
                for provider in obsolete_providers:
                    if provider != p:
                        if provider.name == p.name:
                            reason = "rule_package_same_name"
                        else:
                            reason = "rule_package_implicit_obsoletes"
                        rule = self._create_conflicts_rule(p, provider, reason, str(p))
                        self._add_rule(rule, "package")

    def _add_updated_packages_rules(self, package):
        #print "add updated package rules", package, self.installed_map
        updates = self.policy.find_updated_packages(self.pool, self.installed_map, package)
        #print updates
        for update in updates:
            self._add_package_rules(update)

    def _add_install_job_rules(self, job):
        if len(job.packages) < 1:
            return

        for package in job.packages:
            if not package in self.installed_map:
                self._add_package_rules(package)

        rule = self._create_install_one_rule(job.packages, "job_install", job)
        self._add_rule(rule, "job")

    def _add_job_rules(self):
        for job in self.request.jobs:
            if job.job_type == "install":
                self._add_install_job_rules(job)
