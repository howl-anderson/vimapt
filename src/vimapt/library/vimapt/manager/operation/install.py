from vimapt.manager.executor.install import InstallExecutor
from vimapt.manager.operation.operation import Operation


class Install(Operation):
    def do_execute(self, package):
        InstallExecutor(self.vim_dir).execute(package.package.name)