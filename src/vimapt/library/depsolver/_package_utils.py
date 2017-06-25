import re

from .errors \
    import \
        DepSolverError

_FULL_PACKAGE_RE = re.compile("""\
                              (?P<name>[^-.]+)
                              -
                              (?P<version>(.*))
                              $""", re.VERBOSE)

_PACKAGE_NAME_RE = re.compile("[^-.]+")

def is_valid_package_name(name):
    """
    Returns True if the given string is a valid package name, False
    otherwise.
    """
    return _PACKAGE_NAME_RE.match(name) is not None

def parse_package_full_name(full_name):
    """
    Parse a package full name (e.g. 'numpy-1.6.0') into a (name,
    version_string) pair.
    """
    m = _FULL_PACKAGE_RE.match(full_name)
    if m:
        return m.group("name"), m.group("version")
    else:
        raise DepSolverError("Invalid package full name %s" % (full_name,))

