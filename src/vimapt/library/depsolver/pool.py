import collections

from .bundled.traitlets \
    import \
        HasTraits, Dict, Instance, List, Long, Unicode
from .errors \
    import \
        DepSolverError, MissingPackageInfoInPool
from .package \
    import \
        PackageInfo
from .repository \
    import \
        Repository
from .requirement \
    import \
        Requirement
from .utils \
    import \
        CachedScheduler

MATCH_NONE = 0
MATCH_NAME = 1
MATCH = 2
MATCH_PROVIDE = 3
MATCH_REPLACE = 4

class Pool(HasTraits):
    """Pool objects model a pool of repositories.

    Pools are able to find packages that provide a given requirements (handling
    the provides concept from package metadata).
    """
    repositories = List(Instance(Repository))

    _packages_by_id = Dict()
    _packages_by_name = Dict()

    _id = Long(1)

    _repository_by_name = Instance(collections.defaultdict)
    _scheduler = Instance(CachedScheduler)

    def __init__(self, repositories=None, **kw):
        scheduler = CachedScheduler()
        repository_by_name = collections.defaultdict(list)
        super(Pool, self).__init__(self, _scheduler=scheduler,
                _repository_by_name=repository_by_name, **kw)
        if repositories is None:
            repositories = []

        # provide.name -> package mapping
        self._packages_by_name = collections.defaultdict(list)

        if len(repositories) > 0:
            for repository in repositories:
                self.add_repository(repository)

    def has_package(self, package):
        package_id = package.id
        return package_id in self._packages_by_id

    def add_repository(self, repository):
        """Add a repository to this pool.

        Arguments
        ---------
        repository: Repository
            repository to add
        """
        self.repositories.append(repository)
        self._repository_by_name[repository.name].append(repository)

        for package in repository.iter_packages():
            package.id = self._id
            self._id += 1
            self._packages_by_id[package.id] = package

            self._packages_by_name[package.name].append(package)
            for provide in package.provides:
                self._packages_by_name[provide.name].append(package)
            for replace in package.replaces:
                self._packages_by_name[replace.name].append(package)

    def package_by_id(self, package_id):
        """Retrieve a package from its id.

        Arguments
        ---------
        package_id: str
            A package id
        """
        try:
            return self._packages_by_id[package_id]
        except KeyError:
            raise MissingPackageInfoInPool(package_id)

    def what_provides(self, requirement, mode='composer'):
        """Returns a list of packages that provide the given requirement.

        Arguments
        ---------
        requirement: Requirement
            the requirement to match
        mode: str
            One of the following string:

                - 'composer': behaves like Composer does, i.e. only returns
                  packages that match this requirement directly, unless no
                  match is found in which case packages that provide the
                  requirement indirectly are returned.
                - 'direct_only': only returns packages that match this
                  requirement directly (i.e. provides are ignored).
                - 'include_indirect': only returns packages that match this
                  requirement directly or indirectly (i.e. includes packages
                  that provides this package)
        """
        # FIXME: this is conceptually copied from whatProvides in Composer, but
        # I don't understand why the policy of preferring non-provided over
        # provided packages is handled here.
        if not mode in ['composer', 'direct_only', 'include_indirect']:
            raise ValueError("Invalid mode %r" % mode)

        strict_matches = []
        provided_match = []
        name_match = False

        for package in self._packages_by_name[requirement.name]:
            match = self.matches(package, requirement)
            if match == MATCH_NONE:
                pass
            elif match == MATCH_NAME:
                name_match = True
            elif match == MATCH:
                name_match = True
                strict_matches.append(package)
            elif match == MATCH_PROVIDE:
                provided_match.append(package)
            elif match == MATCH_REPLACE:
                strict_matches.append(package)
            else:
                raise ValueError("Invalid match type: {}".format(match))

        if mode == 'composer':
            if name_match:
                return strict_matches
            else:
                return strict_matches + provided_match
        elif mode == 'direct_only':
            return strict_matches
        elif mode == 'include_indirect':
            return strict_matches + provided_match

    def matches(self, candidate, requirement):
        """Checks whether the candidate package matches the requirement, either
        directly or through provides.

        Arguments
        ---------
        candidate: PackageInfo
            Candidate package
        requirement: Requirement
            The requirement to match

        Returns
        -------
        match_type: _Match or False
            An instance of Match, that specified the type of match:

                - if only the name matches, will be MATCH_NAME
                - if the name and version actually match, will be MATCH
                - if the match is through the package's provides, will be MATCH_PROVIDE
                - if no match at all, will be False

        Examples
        --------
        >>> from depsolver import PackageInfo, Requirement
        >>> R = Requirement.from_string
        >>> pool = Pool()
        >>> pool.matches(PackageInfo.from_string('numpy-1.3.0'), R('numpy >= 1.2.0')) == MATCH
        True
        """
        if requirement.name == candidate.name:
            candidate_requirement = Requirement.from_package_string(candidate.unique_name, candidate.version_factory)
            if requirement.is_universal or candidate_requirement.matches(requirement):
                return MATCH
            else:
                return MATCH_NAME
        else:
            for provide in candidate.provides:
                if requirement.matches(provide):
                    return MATCH_PROVIDE

            for replace in candidate.replaces:
                if requirement.matches(replace):
                    return MATCH_REPLACE

            return MATCH_NONE

    def id_to_string(self, package_id):
        """
        Convert a package id to a nice string representation.
        """
        package = self.package_by_id(abs(package_id))
        if package_id > 0:
            return "+" + str(package)
        else:
            return "-" + str(package)

    #------------------------
    # Repository priority API
    #------------------------
    def set_repository_order(self, repository_name, after=None, before=None):
        candidates = self._repository_by_name[repository_name]
        if len(candidates) < 1:
            raise DepSolverError("No repository with name '%s'" % (repository_name,))
        else:
            self._scheduler.set_constraints(repository_name, after, before)

    def repository_priority(self, repository):
        """
        Returns the priority of a repository.

        Priorities are in the ]-inf, 0] integer range, and the ordering is the
        same as integers: the lower the priority number, the less a repository
        has priority over other repositories.

        If no constraint has been set up for the repository, its priority is 0.

        Parameters
        ----------
        repository: Repository
            The repository to compute the priority of.
        """
        if repository.name in self._repository_by_name:
            priorities = self._scheduler.compute_priority()
            # We return a negative number to follow Composer convention.
            return priorities.get(repository.name, 0) - (len(priorities) - 1)
        else:
            raise DepSolverError("Unknown repository name '%s'" % (repository.name,))
