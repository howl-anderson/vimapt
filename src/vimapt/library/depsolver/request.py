from .bundled.traitlets \
    import \
        HasTraits, Enum, Instance, List
from .requirement \
    import \
        Requirement
from .package \
    import \
        PackageInfo
from .pool \
    import \
        Pool

class _Job(HasTraits):
    packages = List(Instance(PackageInfo))
    job_type = Enum(["install", "remove", "update", "upgrade"])
    requirement = Instance(Requirement)

    def __init__(self, packages, job_type, requirement, **kw):
        if packages is None:
            packages = packages
        super(_Job, self).__init__(packages=packages, job_type=job_type,
                                   requirement=requirement, **kw)

    def __eq__(self, other):
        if other is None:
            return False
        if len(self.packages) != len(other.packages):
            return False
        else:
            for left, right in zip(self.packages, other.packages):
                if left != right:
                    return False
            return self.job_type == other.job_type \
                    and self.requirement == other.requirement

class Request(HasTraits):
    """A Request instance encompasses the set of jobs to be solved by the
    dependency solver.
    """
    pool = Instance(Pool)

    _jobs = List(Instance(Pool))

    def __init__(self, pool, **kw):
        super(Request, self).__init__(pool=pool, _jobs=[], **kw)

    @property
    def jobs(self):
        return self._jobs

    def _add_job(self, requirement, job_type):
        packages = self.pool.what_provides(requirement)

        self.jobs.append(_Job(packages, job_type, requirement))

    def install(self, requirement):
        self._add_job(requirement, "install")

    def update(self, requirement):
        self._add_job(requirement, "update")

    def remove(self, requirement):
        self._add_job(requirement, "remove")

    def upgrade(self):
        self.jobs.append(_Job([], "upgrade", None))
