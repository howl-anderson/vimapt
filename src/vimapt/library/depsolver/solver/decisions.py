import collections

import six

from ..compat \
    import \
        OrderedDict
from ..bundled.traitlets \
    import \
        HasTraits, Dict, Instance
from ..errors \
    import \
        DepSolverError

from ..pool \
    import \
        Pool

Decision = collections.namedtuple("Decision", ["literal", "reason"])

class DecisionsSet(HasTraits):
    """A DecisionsSet instance keeps track of decided literals (and the
    rational for each decision), and can infer new literals depending on
    their type."""
    pool = Instance(Pool)

    # Package id -> decision level mapping
    _decision_map = Instance(OrderedDict)

    # Queue of Decision instances
    _decision_queue = Instance(collections.deque)

    @property
    def last_literal(self):
        return self._decision_queue[-1].literal

    @property
    def last_reason(self):
        return self._decision_queue[-1].reason

    def __init__(self, pool, **kw):
        super(DecisionsSet, self).__init__(self, pool=pool, **kw)
        self._decision_map = OrderedDict()
        self._decision_queue = collections.deque()

    def decide(self, literal, level, why):
        """
        Add the given literal to the decision set at the given level.

        Parameters
        ----------
        literal: int
            Package id
        level: int
            Level
        why: str
            Rational for the decision
        """
        self._add_decision(literal, level)
        self._decision_queue.append(Decision(literal, why))

    def satisfy(self, literal):
        """
        Return True if ths given literal is satisfied
        """
        package_id = abs(literal)
        positive_case = literal > 0 and package_id in self._decision_map \
                and self._decision_map[package_id] > 0
        negative_case = literal < 0 and package_id in self._decision_map \
                and self._decision_map[package_id] < 0
        return positive_case or negative_case

    def conflict(self, literal):
        """
        Return True if the given literal conflicts with the decision set.
        """
        package_id = abs(literal)

        positive_case = literal > 0 and package_id in self._decision_map \
                and self._decision_map[package_id] < 0
        negative_case = literal < 0 and package_id in self._decision_map \
                and self._decision_map[package_id] > 0
        return positive_case or negative_case

    def is_decided(self, literal):
        """
        Return True if the given literal has been decided at any level.
        """
        return self._decision_map.get(abs(literal), 0) != 0

    def is_undecided(self, literal):
        """
        Return True if the given literal has not been decided at any level.
        """
        return self._decision_map.get(abs(literal), 0) == 0

    def is_decided_install(self, literal):
        package_id = abs(literal)
        return self._decision_map.get(package_id, 0) > 0

    def decision_level(self, literal):
        """
        Returns the decision level of the given literal.

        If the literal is not decided yet, returns 0.
        """
        package_id = abs(literal)
        if package_id in self._decision_map:
            return abs(self._decision_map[package_id])
        else:
            return 0

    def at_offset(self, offset):
        return self._decision_queue[offset]

    def is_offset_valid(self, offset):
        return offset >= 0 and offset < len(self._decision_queue)

    def revert_last(self):
        self._decision_map[abs(self.last_literal)] = 0
        self._decision_queue.pop()

    #------------
    # Private API
    #------------
    def _add_decision(self, literal, level):
        package_id = abs(literal)

        if package_id in self._decision_map:
            previous_decision = self._decision_map[package_id]
            literal_string = self.pool.id_to_string(package_id)
            package = self.pool.package_by_id(package_id)

            raise DepSolverError("Trying to decide %s on level %d, even though "
                    "%s was previously decided as %d" % (literal_string, level,
                        package, previous_decision))
        else:
            if literal > 0:
                self._decision_map[package_id] = level
            else:
                self._decision_map[package_id] = -level

    #------------------
    # Sequence protocol
    #------------------
    def __contains__(self, literal):
        return literal in self._decision_map

    def __len__(self):
        return len(self._decision_queue)

    #------------------
    # Iterator protocol
    #------------------
    # We return a reversed iterator to follow composer behavior, not sure about
    # the rationale
    def __iter__(self):
        return reversed(self._decision_queue)
