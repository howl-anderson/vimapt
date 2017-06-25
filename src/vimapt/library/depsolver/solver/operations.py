class Operation(object):
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

class Update(Operation):
    def __init__(self, from_package, to_package, reason=None):
        self.from_package = from_package
        self.to_package = to_package
        self.reason = None

    def __repr__(self):
        return "Updating %s (%s) to %s (%s)" % (
                self.from_package.name, self.from_package.version,
                self.to_package.name, self.to_package.version)

class Install(Operation):
    def __init__(self, package, reason=None):
        self.package = package
        self.reason = reason

    def __repr__(self):
        return "Installing %s (%s)" % (self.package.name, self.package.version)

class Uninstall(Operation):
    def __init__(self, package, reason=None):
        self.package = package
        self.reason = reason

    def __repr__(self):
        return "Uninstalling %s (%s)" % (self.package.name, self.package.version)
