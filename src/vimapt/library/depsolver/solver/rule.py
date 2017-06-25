import hashlib
import re

import six

from ..bundled.traitlets \
    import \
        HasTraits, Bool, Enum, Instance, List, Long, Unicode
from ..errors \
    import \
        DepSolverError, MissingPackageInfoInPool
from .._package_utils \
    import \
        is_valid_package_name
from ..package \
    import \
        PackageInfo
from ..pool \
    import \
        Pool
from ..request \
    import \
        _Job
from ..requirement \
    import \
        Requirement
from ..version \
    import \
        SemanticVersion, Version

_RULE_REASONS = [
    "internal_allow_update",
    "job_install",
    "job_remove",
    "package_conflict",
    "package_requires",
    "package_obsoletes",
    "rule_installed_package_obsoletes",
    "rule_package_same_name",
    "rule_package_implicit_obsoletes",
    "rule_learned",
    "rule_package_alias",
]

class PackageRule(HasTraits):
    """A Rule where literals are package ids attached to a pool.

    It essentially allows for pretty-printing package names instead of internal
    ids as used by the SAT solver underneath.
    """
    pool = Instance(Pool)
    literals = List(Long)

    reason = Enum(_RULE_REASONS)
    reason_details = Unicode("")

    job = Instance(_Job)

    enabled = Bool(True)

    id = Long(-1)
    rule_type = Enum(["unknown", "packages", "job", "learnt"])

    _rule_hash = Unicode("")

    @classmethod
    def from_string(cls, pool, rule_string, reason, reason_details="", job=None, id=-1):
        """
        Creates a PackageRule from a rule string, e.g. '-numpy-1.6.0 | numpy-1.7.0'

        Because package full name -> id is not 1-to-1 mapping, this may fail
        when a package has multiple ids. This is mostly used for testing, to
        write reference rules a bit more easily.
        """
        packages_string = (s.strip() for s in rule_string.split("|"))
        package_literals = []
        for package_string in packages_string:
            if package_string.startswith("-"):
                positive = False
                package_string = package_string[1:]
            else:
                positive = True

            requirement = Requirement.from_package_string(package_string)
            package_candidates = pool.what_provides(requirement)
            if len(package_candidates) == 0:
                raise ValueError("No candidate for package %s" % package_string)
            elif len(package_candidates) > 1:
                msg = "> 1 candidate for package %s requirement, cannot " \
                      "create rule from it" % package_string
                raise ValueError(msg)
            else:
                if positive:
                    package_literals.append(package_candidates[0].id)
                else:
                    package_literals.append(-package_candidates[0].id)

        return cls(pool, package_literals, reason, reason_details, job, id)

    @classmethod
    def from_packages(cls, pool, packages, reason, reason_details="", job=None, id=-1):
        literals = [p.id for p in packages]
        if len(packages) > 0:
            return cls(pool, literals, reason, reason_details, job, id, packages[0].version_factory)
        else:
            return cls(pool, literals, reason, reason_details, job, id)

    def __init__(self, pool, literals, reason, reason_details="", job=None,
                 id=-1, version_factory=SemanticVersion.from_string, **kw):
        if reason == "job_install":
            if not is_valid_package_name(reason_details):
                raise DepSolverError(
                        "reason_details must be a valid package name for "
                        "'job_install' rule")
        elif reason == "package_requires":
            try:
                Requirement.from_string(reason_details, version_factory=version_factory)
            except Exception:
                raise DepSolverError("Invalid requirement string '%s'" % (reason_details,))

        literals = sorted(literals)
        super(PackageRule, self).__init__(pool=pool, literals=literals,
                reason=reason, reason_details=reason_details, job=job, id=id,
                **kw)

    @property
    def rule_hash(self):
        # The exact rule hash algorithm is copied from composer
        data = ",".join(str(i) for i in self.literals)
        return hashlib.md5(data.encode('ascii')).hexdigest()[:5]

    @property
    def is_assertion(self):
        return len(self.literals) == 1

    @property
    def required_package_name(self):
        if self.reason == "job_install":
            return self.reason_data
        elif self.reason == "package_requires":
            return Requirement.from_string(self.reason_data)
        else:
            return ""

    def is_equivalent(self, other):
        """Two rules are considered equivalent if they have the same
        literals."""
        if not isinstance(other, PackageRule):
            return NotImplemented
        return self.literals == other.literals

    def __str__(self):
        return "(%s)" % " | ".join(self.pool.id_to_string(l) for l in self.literals)

    def __repr__(self):
        return "PackageRule('%s', '%s', '%s')" % \
                (" | ".join(self.pool.id_to_string(l) for l in self.literals),
                 self.reason, self.reason_details)


    def __eq__(self, other):
        return repr(self) == repr(other) and self.reason == other.reason \
                and self.reason_details == other.reason_details
