import collections
import copy

import six

from .errors \
    import \
        DepSolverError
from .bundled.traitlets \
    import \
        TraitType, Undefined

def _invert_dependencies(deps):
    """Given a dictionary of edge -> dependencies representing a DAG, "invert"
    all the dependencies."""
    ideps = {}
    for k, v in deps.items():
        for d in v:
            l = ideps.get(d, None)
            if l:
                l.append(k)
            else:
                l = [k]
            ideps[d] = l

    return ideps

class Scheduler(object):
    """
    Simple scheduler class to register names with before/after constraints, and
    sort their priority
    """
    def __init__(self):
        # For a given name, self.before[name] list all the jobs that must be
        # completed before name.
        self.before = collections.defaultdict(list)
        self.names = {}

    def _register(self, name):
        if not name in self.names:
            self.names[name] = name

    def set_constraints(self, name, after=None, before=None):
        """
        Set the given name to be scheduled before the `before` argument, and
        after the `after` argument.

        Parameters
        ----------
        name: str
            The name to be scheduled
        after: str
            The job given in `name` will be scheduled after the job in `after`.
        before: str
            The job given in `name` will be scheduled before the job in `before`.
        """
        self._register(name)

        if after is not None:
            self._register(after)
            if not after in self.before[name]:
                self.before[name].append(after)

        if before is not None:
            self._register(before)
            if not name in self.before[before]:
                self.before[before].append(name)

    def order(self, target):
        after = _invert_dependencies(self.before)

        visited = {}
        out = []

        # DFS-based topological sort: this is better to only get the
        # dependencies of a given target command instead of sorting the whole
        # dag
        def _visit(n, stack_visited):
            if n in stack_visited:
                raise DepSolverError("Cycle detected: %r" % after)
            else:
                stack_visited[n] = None
            if not n in visited:
                visited[n] = None
                for m, v in after.items():
                    if n in v:
                        _visit(m, stack_visited)
                out.append(n)
            stack_visited.pop(n)
        _visit(target, {})
        return [self.names[o] for o in out[:-1]]

    def _full_order(self):
        before = copy.deepcopy(self.before)
        res = []
        incoming = set(name for name in self.names if len(self.before[name]) == 0)
        while len(incoming) > 0:
            n = incoming.pop()
            res.append(n)
            for m in (k for k, v in six.iteritems(before) if n in v):
                before[m] = list(set(before[m]).difference([n]))
                if len(before[m]) == 0:
                    incoming.add(m)
        if any([bool(v) for v in six.itervalues(before)]):
            raise DepSolverError("Circular dependency: %s", ([k for k, v in before.iteritems() if v],))
        else:
            return res

    def compute_priority(self):
        """
        Compute the name -> priority dictionary.
        
        if priority['A'] < priority['B'], B has priority over A.
        """
        return dict((name, i) for i, name in enumerate(self._full_order()))

class CachedScheduler(object):
    def __init__(self, scheduler=None):
        if scheduler is None:
            scheduler = Scheduler()
        self._scheduler = scheduler
        self._cached = None

    @property
    def invalidated(self):
        return self._cached is None

    def set_constraints(self, name, after=None, before=None):
        self._cached = None
        self._scheduler.set_constraints(name, after, before)

    def compute_priority(self):
        if self.invalidated:
            res = self._scheduler.compute_priority()
            self._cached = res
        return self._cached

class Callable(TraitType):
    info_text = "a callable object"

    def validate(self, obj, value):
        if value is Undefined or callable(value):
            return value
        else:
            self.error(obj, value)
