"""Simple module that implements the Semantic Version RFC  (v2.0.0.0-rc1 as
this time: http://semver.org)."""
import re

from .errors \
    import \
        InvalidVersion

PART = r"[0-9a-zA-Z-]+"

_INT_PART_RE = re.compile("\d+")

_VERSION_RE = re.compile(r"""
        ^
        (?P<version>\d+.\d+.\d+)                                # minimum 'Major.Minor.Patch' (mandatory)
        (-(?P<pre_release>[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?    # pre-release part (optional)
        (\+(?P<build>[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?         # build part (optional)
        $""", re.VERBOSE)

_LOOSE_VERSION_RE = re.compile(r"""
        ^
        (?P<version>\d+(\.\d+)*)                                 # minimum 'Major' (mandatory)
        (-(?P<pre_release>[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?    # pre-release part (optional)
        (\+(?P<build>[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?         # build part (optional)
        $""", re.VERBOSE)

_PRE_RELEASE_VERSION_RE = re.compile(r"""
        ^
        ({part})(\.{part})*
        $""".format(part=PART), re.VERBOSE)

_BUILD_VERSION_RE = re.compile(r"""
        ^
        ({part})(\.{part})*
        $""".format(part=PART), re.VERBOSE)

def is_version_valid(version_string):
    """Return False if the given string is not a valid version."""
    return _VERSION_RE.match(version_string) is not None

def _is_int_like(int_or_int_string):
    return _INT_PART_RE.match(int_or_int_string) is not None

def _compute_comparable_parts(parts):
    comparable_parts = []
    for part in parts:
        if _is_int_like(part):
            comparable_parts.append(int(part))
        else:
            comparable_parts.append(part)
    return tuple(part for part in comparable_parts)

class PreReleaseVersion(object):
    @classmethod
    def from_string(cls, s):
        m = _PRE_RELEASE_VERSION_RE.match(s)
        if m:
            parts = s.split(".")
            return cls(parts)
        else:
            raise InvalidVersion("String %r is not a valid pre release version" % (s,))

    def __init__(self, parts):
        self.parts = parts
        self._comparable_parts = _compute_comparable_parts(parts)

    def __repr__(self):
        return "PreReleaseVersion(%s)" % (", ".join(repr(part) for part in self.parts))

    def __str__(self):
        return "-%s" % ("-".join(str(part) for part in self.parts))

    # Comparison API
    def _ensure_can_compare(self, other):
        if other and not isinstance(other, PreReleaseVersion):
            raise TypeError("cannot compare %s and %s"
                    % (type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        if other is None:
            return False
        else:
            self._ensure_can_compare(other)
            return self.parts == other.parts

    def __lt__(self, other):
        # No pre-release > pre-release
        if  other is None:
            return True
        else:
            self._ensure_can_compare(other)
            return self._comparable_parts < other._comparable_parts

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self == other or not (self < other)

    def __gt__(self, other):
        return not self <= other

class BuildVersion(object):
    @classmethod
    def from_string(cls, s):
        m = _BUILD_VERSION_RE.match(s)
        if m:
            parts = s.split(".")
            return cls(parts)
        else:
            raise InvalidVersion("String %r is not a valid valid version" % (s,))

    def __init__(self, parts):
        self.parts = parts
        self._comparable_parts = _compute_comparable_parts(parts)

    def __repr__(self):
        return "BuildVersion(%s)" % (", ".join(repr(part) for part in self.parts))

    def __str__(self):
        return "+%s" % ("+".join(str(part) for part in self.parts))

    # Comparison API
    def _ensure_can_compare(self, other):
        if other and not isinstance(other, BuildVersion):
            raise TypeError("cannot compare %s and %s"
                    % (type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        if other is None:
            return False
        else:
            self._ensure_can_compare(other)
            return self.parts == other.parts

    def __lt__(self, other):
        if other is None:
            return False
        else:
            self._ensure_can_compare(other)
            return self._comparable_parts < other._comparable_parts

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self == other or not (self < other)

    def __gt__(self, other):
        return not self <= other

class Version(object):
    pass

class SemanticVersion(Version):
    """Create a SemanticVersion instance

    Instances represent a full version according to the semantic version specs
    (version 2.0.0-rc1 of the spec). The main features of this class are
    validation and version comparison.

    Arguments
    ---------
    major: int
        The major number
    minor: int
        The minor number
    patch: int
        The patch (or micro) number
    pre_release: PreReleaseVersion
        The pre release part of the version
    build: BuildVersion
        The build version part of the version
    """
    @classmethod
    def from_string(cls, version_string):
        """Creates a SemanticVersion instance from a string specifiction

        Arguments
        ---------
        version_string: str
            The string version

        Examples
        --------
        >>> v = SemanticVersion.from_string("1.3.1")
        >>> v = SemanticVersion.from_string("1.3.1-dev2+post1")
        """
        if not is_version_valid(version_string):
            raise InvalidVersion("Version string %r is not valid" % (version_string,))
        else:
            m = _VERSION_RE.match(version_string)
            version = m.group("version")
            major, minor, patch = version.split(".")
            pre_release = m.group("pre_release")
            if pre_release is not None:
                pre_release = PreReleaseVersion.from_string(pre_release)
            build = m.group("build")
            if build is not None:
                build = BuildVersion.from_string(build)

            return cls(major, minor, patch, pre_release, build)

    def __init__(self, major, minor, patch, pre_release=None, build=None):
        try:
            #: The major number version
            self.major = int(major)
        except ValueError:
            raise InvalidVersion("Invalid major version %r" % (major,))

        try:
            #: The minor number version
            self.minor = int(minor)
        except ValueError:
            raise InvalidVersion("Invalid minor version %r" % (minor,))

        try:
            #: The patch number version
            self.patch = int(patch)
        except ValueError:
            raise InvalidVersion("Invalid patch version %r" % (patch,))

        if pre_release and not isinstance(pre_release, PreReleaseVersion):
            raise InvalidVersion("pre_release expected to be a PreReleaseVersion instance: %r" % (pre_release,))
        #: The pre_release number version
        self.pre_release = pre_release

        if build and not isinstance(build, BuildVersion):
            raise InvalidVersion("build expected to be a BuildVersion instance: %r" % (build,))
        self.build = build

        self.parts = [self.major, self.minor, self.patch]
        if self.pre_release:
            self.parts.append(self.pre_release.parts)
        if self.build:
            self.parts.append(self.build.parts)

        self._comparable_parts = [self.major, self.minor, self.patch]
        self._comparable_parts.append(self.pre_release)
        self._comparable_parts.append(self.build)

    # Comparison API
    def _ensure_can_compare(self, other):
        if not isinstance(other, Version):
            raise TypeError("cannot compare %s and %s"
                    % (type(self).__name__, type(other).__name__))

    def __repr__(self):
        s = "SemanticVersion(%s, %s, %s" % (self.major, self.minor, self.patch)
        if self.pre_release:
            s += ", %r" % (self.pre_release,)
        if self.build:
            s += ", %r" % (self.build,)
        s += ")"
        return s

    def __str__(self):
        s = "%s.%s.%s" % (self.major, self.minor, self.patch)
        if self.pre_release:
            s += str(self.pre_release)
        if self.build:
            s += str(self.build)
        return s

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        self._ensure_can_compare(other)
        return self._comparable_parts == other._comparable_parts

    def __ne__(self, other):
        if other is None:
            return True
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        self._ensure_can_compare(other)
        return self._comparable_parts < other._comparable_parts

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self < other or self == other)

    def __ge__(self, other):
        return self > other or self == other

class MinVersion(Version):
    """Subclass of Version such as MinVersion() < v for any Version instance v
    (unless v is MinVersion()."""
    def __eq__(self, other):
        return other.__class__ == self.__class__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return not self == other

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return self == other

    def __hash__(self):
        return hash("MinVersion")

class MaxVersion(Version):
    """Subclass of Version such as MaxVersion() > v for any Version instance v
    (unless v is MaxVersion()."""
    def __eq__(self, other):
        return other.__class__ == self.__class__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return self == other

    def __gt__(self, other):
        return not self == other

    def __ge__(self, other):
        return True

    def __hash__(self):
        return hash("MaxVersion")
