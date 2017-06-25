import re

from .errors \
    import \
        InvalidVersion
from .version \
    import \
        Version

class EnpkgVersion(Version):
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
        comparable_parts.append(upstream)
        if revision is None:
            comparable_parts.append("0")
        else:
            comparable_parts.append(revision)
        self._comparable_parts = comparable_parts

    def __str__(self):
        s = self.upstream
        if self.epoch:
            s = self.epoch + ":" + s
        if self.revision:
            s += "~" + self.revision
        return s

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, DebianVersion):
            return self._comparable_parts == other._comparable_parts
        else:
            return NotImplemented
