from vimapt.manager.executor.remove import RemoveExecutor
from vimapt.manager.operation.operation import Operation


class Remove(Operation):
    def do_execute(self, package):
        RemoveExecutor(self.vim_dir).execute(package.package.name)