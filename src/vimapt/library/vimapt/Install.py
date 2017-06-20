#!/usr/bin/env python

import logging

from vimapt.manager.manage_action import ManageAction
from vimapt.manager.manager import Manager

logger = logging.getLogger(__name__)


class Install(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir  # user's .vim dir path
        self.manager = Manager(vim_dir)

    def repo_install(self, package_name):
        self.manager.execute(ManageAction.INSTALL, package_name)
