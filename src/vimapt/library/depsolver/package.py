import collections
import re

import six

from .compat \
    import \
        OrderedDict
from ._package_utils \
    import \
        parse_package_full_name
from .requirement \
    import \
        Requirement
from .requirement_parser \
    import \
        RawRequirementParser
from .utils \
    import \
        Callable
from .version \
    import \
        SemanticVersion, Version
from .bundled.traitlets \
    import \
        HasTraits, Instance, List, Long, Unicode

R = Requirement.from_string

_DEPENDENCY_TYPES = ["depends", "provides", "replaces", "conflicts", "suggests"]
_SECTION_RE = re.compile("""\
        (%(dependency_types)s)
        \s*
        \(
            (.*)
        \)
""" % {"dependency_types": "|".join(_DEPENDENCY_TYPES)}, re.VERBOSE)


def _parse_name_version_part(name_version, version_factory):
    name, version_string = parse_package_full_name(name_version)
    version = version_factory(version_string)
    return name, version

def _parse_requirements_string(parser, s, version_factory):
    m = _SECTION_RE.search(s)
    if m is None:
        raise ValueError("invalid requirement string: %r" % s)
    else:
        requirements_type, requirements_string = m.groups()
        requirements = OrderedDict()
        for requirement_string in requirements_string.split(","):
            for distribution_name, specs in parser.parse(requirement_string).items():
                if not distribution_name in requirements:
                    requirements[distribution_name] = []
                requirements[distribution_name].extend(specs)
        return requirements_type, \
               [Requirement(name, reqs, version_factory)
                for name, reqs in six.iteritems(requirements)]

def parse_package_string(package_string, version_factory):
    parser = RawRequirementParser()

    parts = package_string.split(";")
    name, version = _parse_name_version_part(parts[0], version_factory)

    requirements_lists = collections.defaultdict(list)
    for part in parts[1:]:
        requirement_type, requirements = _parse_requirements_string(parser, part, version_factory)
        requirements_lists[requirement_type].extend(requirements)

    provides = requirements_lists["provides"]
    depends = requirements_lists["depends"]
    conflicts = requirements_lists["conflicts"]
    replaces = requirements_lists["replaces"]
    suggests = requirements_lists["suggests"]

    return name, version, provides, depends, conflicts, replaces, suggests

class PackageInfo(HasTraits):
    """
    PackageInfoInfo instances contain exactly all the metadata needed for the
    dependency management.

    Parameters
    ----------
    name: str
        Name of the package (i.e. distribution name)
    version: object
        Instance of Version
    provides: None or sequence
        Sequence of Requirements.
    dependencies: None or sequence
        Sequence of Requirements.
    """
    name = Unicode()
    version = Instance(Version)
    version_factory = Callable()

    dependencies = List(Instance(Requirement))
    provides = List(Instance(Requirement))
    conflicts = List(Instance(Requirement))
    replaces = List(Instance(Requirement))
    suggests = List(Instance(Requirement))

    id = Long(-1)

    _repository = Instance("depsolver.repository.Repository")

    @classmethod
    def from_string(cls, package_string, version_factory=SemanticVersion.from_string):
        """Create a new package from a string.

        Example
        -------
        >>> P = PackageInfo.from_string
        >>> P("numpy-1.3.0; depends (mkl <= 10.4.0, mkl >= 10.3.0)")
        PackageInfo(u'numpy-1.3.0; depends (mkl >= 10.3.0, mkl <= 10.4.0)')
        >>> numpy_1_3_0 = PackageInfo("numpy", Version.from_string("1.3.0"))
        >>> P("numpy-1.3.0") == numpy_1_3_0
        True
        """
        name, version, provides, dependencies, conflicts, replaces, suggests \
                = parse_package_string(package_string, version_factory)
        return cls(name=name, version=version, version_factory=version_factory,
                   provides=list(provides),
                   dependencies=list(dependencies), conflicts=list(conflicts),
                   replaces=list(replaces), suggests=list(suggests))

    def __init__(self, name, version,
            version_factory=SemanticVersion.from_string, dependencies=None,
            provides=None, conflicts=None, replaces=None, suggests=None, **kw):
        if dependencies is None:
            dependencies = []
        if provides is None:
            provides = []
        if conflicts is None:
            conflicts = []
        if replaces is None:
            replaces = []
        if suggests is None:
            suggests = []
        super(PackageInfo, self).__init__(name=name, version=version,
                                          version_factory=version_factory,
                                          dependencies=dependencies,
                                          provides=provides,
                                          conflicts=conflicts,
                                          replaces=replaces,
                                          suggests=suggests,
                                          **kw)
    @property
    def unique_name(self):
        return self.name + "-" + str(self.version)

    @property
    def package_string(self):
        strings = ["%s-%s" % (self.name, self.version)]
        if self.dependencies:
            strings.append("depends (%s)" % ", ".join(str(s) for s in self.dependencies))
        if self.provides:
            strings.append("provides (%s)" % ", ".join(str(s) for s in self.provides))
        if self.conflicts:
            strings.append("conflicts (%s)" % ", ".join(str(s) for s in self.conflicts))
        if self.replaces:
            strings.append("replaces (%s)" % ", ".join(str(s) for s in self.replaces))
        if self.suggests:
            strings.append("suggests (%s)" % ", ".join(str(s) for s in self.suggests))
        return "; ".join(strings)

    @property
    def repository(self):
        return self._repository

    @repository.setter
    def repository(self, repository):
        if self._repository is not None:
            raise ValueError("Repository for this package is already set to %s!" % \
                             format(self._repository))
        self._repository = repository

    def __repr__(self):
        return "PackageInfo(%r)" % self.package_string

    def __str__(self):
        return self.unique_name

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version \
                and self.provides == other.provides \
                and self.dependencies == other.dependencies \
                and self.id == other.id

    def __hash__(self):
        return hash("%s%d" % (str(self), self.id))
