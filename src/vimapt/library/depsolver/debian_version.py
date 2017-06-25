import re

import six

from .compat \
    import \
        izip_longest
from .errors \
    import \
        InvalidVersion
from .version \
    import \
        Version

_EPOCH_RE = re.compile("\d")

_UPSTREAM_VERSION_RE = re.compile("\d[a-zA-Z0-9.+-:~]*")

_DEBIAN_REVISION_RE = re.compile("[a-zA-Z0-9+.~]+")

_DIGITS_NO_DIGITS_RE = re.compile("(\d*)(\D*)")

def _compute_comparable():
    comparable = dict((c, ord(c)) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    comparable["~"] = -1
    comparable[""] = 0
    for k in ".+-:":
        comparable[k] = ord(k) + 256
    return comparable

_COMPARABLE = _compute_comparable()

def parse_version_string(version):
    epoch = None
    revision = None

    if ":" in version:
        epoch, version = version.split(":", 1)
    if "-" in version:
        version, revision = version.split("-", 1)

    if epoch is not None and not _EPOCH_RE.match(epoch):
        raise InvalidVersion("Invalid epoch for debian version: '%s'" % epoch)
    if not _UPSTREAM_VERSION_RE.match(version):
        raise InvalidVersion("Invalid upstream version for debian version: '%s'" % version)
    if revision is not None and not _DEBIAN_REVISION_RE.match(revision):
        raise InvalidVersion("Invalid debian revision for debian version: '%s'" % revision)

    return epoch, version, revision

def is_valid_debian_version(version):
    """
    Return True if the given version is a valid debian version
    """
    try:
        parse_version_string(version)
        return True
    except InvalidVersion:
        return False

if six.PY3:
    def _cmp(x, y):
        return (x > y) - (x < y)
else:
    _cmp = cmp

def _compare_part(left, right):
    """
    Compare two version strings according to the Debian comparison algorithm.

    Parameters
    ----------
    left: str
    right: str
        left and right version parts. A part must be either an upstream version
        or a debian revision

    Returns
    -------
    ret: int
        -1, 0 or 1 depending on the result of the comparison
    """
    left_parts = _DIGITS_NO_DIGITS_RE.split(left)
    right_parts = _DIGITS_NO_DIGITS_RE.split(right)

    for left_part, right_part in izip_longest(left_parts, right_parts, fillvalue=""):
        try:
            left_part, right_part = int(left_part), int(right_part)
        except ValueError:
            for left_part_c, right_part_c in izip_longest(left_part, right_part, fillvalue=""):
                st = _cmp(_COMPARABLE[left_part_c], _COMPARABLE[right_part_c])
                if st != 0:
                    return st
        else:
            st = _cmp(left_part, right_part)
            if st != 0:
                return st
    return 0

class ComparablePart(object):
    def __init__(self, version):
        self._version = version

    def __eq__(self, other):
        if isinstance(other, ComparablePart):
            return _compare_part(self._version, other._version) == 0
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ComparablePart):
            return _compare_part(self._version, other._version) == -1
        else:
            return NotImplemented

    def __cmp__(self, other):
        if isinstance(other, ComparablePart):
            return _compare_part(self._version, other._version)
        else:
            return NotImplemented

class DebianVersion(Version):
    @classmethod
    def from_string(cls, version):
        epoch, upstream, revision = parse_version_string(version)
        return cls(upstream, revision, epoch)

    def __init__(self, upstream, revision=None, epoch=None):
        self.upstream = upstream
        self.revision = revision
        self.epoch = epoch

        comparable_parts = []
        if epoch is None:
            comparable_parts.append(0)
        else:
            comparable_parts.append(int(epoch))
        comparable_parts.append(ComparablePart(upstream))
        if revision is None:
            comparable_parts.append(ComparablePart("0"))
        else:
            comparable_parts.append(ComparablePart(revision))
        self._comparable_parts = comparable_parts

    def __str__(self):
        s = self.upstream
        if self.epoch:
            s = self.epoch + ":" + s
        if self.revision:
            s += "-" + self.revision
        return s

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        if isinstance(other, DebianVersion):
            return cmp(self._comparable_parts, other._comparable_parts)
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, DebianVersion):
            return self._comparable_parts == other._comparable_parts
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DebianVersion):
            return self._comparable_parts < other._comparable_parts
        else:
            return NotImplemented

if six.PY3:
    import functools
    ComparablePart = functools.total_ordering(ComparablePart)
    DebianVersion = functools.total_ordering(DebianVersion)
