class _Constraint(object):
    def __repr__(self):
        return "%s" % self.__class__.__name__

    # Mostly useful for testing
    def __eq__(self, other):
        return self.__class__ == other.__class__

class Any(_Constraint):
    pass

class _VersionConstraint(_Constraint):
    def __init__(self, version):
        self.version = version

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.version)

    # Mostly useful for testing
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.version == other.version

    def __hash__(self):
        return hash(repr(self))

class Equal(_VersionConstraint):
    pass

class Not(_VersionConstraint):
    pass

class GEQ(_VersionConstraint):
    pass

class GT(_VersionConstraint):
    pass

class LEQ(_VersionConstraint):
    pass

class LT(_VersionConstraint):
    pass
