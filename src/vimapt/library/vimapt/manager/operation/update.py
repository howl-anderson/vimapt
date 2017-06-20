from vimapt.manager.operation.remove import Remove
from vimapt.manager.operation.install import Install
from vimapt.manager.operation.operation import Operation


class Update(Operation):
    def do_execute(self, package):
        Remove(self.vim_dir).execute(package.from_package.name)
        Install(self.vim_dir).execute(package.to_package.name)