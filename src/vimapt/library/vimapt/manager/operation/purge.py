from vimapt.manager.executor.purge import PurgeExecutor
from vimapt.manager.operation.operation import Operation


class Purge(Operation):
    def execute(self, package):
        PurgeExecutor(self.vim_dir).execute(package.package.name)