import logging

from depsolver.solver.operations import (
    Install as InstallOperation,
    Uninstall as UninstallOperation,
    Update as UpdateOperation
)

from vimapt.manager.dependency_solver.solver import DependencySolver
from vimapt.manager.operation.install import Install
from vimapt.manager.operation.uninstall import Uninstall
from vimapt.manager.operation.update import Update

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

        self.solver = DependencySolver(self.vim_dir)
        self.installer = Install(self.vim_dir)
        self.uninstaller = Uninstall(self.vim_dir)
        self.updater = Update(self.vim_dir)

    def execute(self, action, target):
        logger.info("Start process {}: {}".format(action, target))

        operation_list = self.solver.solve(action, target)

        logger.info("Operation list: {}".format(operation_list))

        for operation in operation_list:
            if isinstance(operation, InstallOperation):
                logger.info("Dispatch operation {}: {}".format(type(operation), operation))
                self.installer.execute(operation)
            if isinstance(operation, UninstallOperation):
                logger.info("Dispatch operation {}: {}".format(type(operation), operation))
                self.uninstaller.execute(operation)
            if isinstance(operation, UpdateOperation):
                logger.info("Dispatch operation {}: {}".format(type(operation), operation))
                self.updater.execute(operation)

        logger.info("End process {}: {}".format(action, target))
