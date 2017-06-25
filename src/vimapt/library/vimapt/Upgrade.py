#!/usr/bin/env python

import logging
import os

from vimapt.manager.manage_action import ManageAction
from vimapt.manager.manager import Manager

logger = logging.getLogger(__name__)


class Upgrade(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir  # user's .vim dir path
        self.manager = Manager(vim_dir)

    def upgrade_package(self, package_name):
        self.manager.execute(ManageAction.SOFT_UPDATE, package_name)

    def upgrade_all(self):
        self.manager.execute(ManageAction.UPDATE_ALL)

    def get_installed_package_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            absolute_file_path = os.path.join(record_dir, f)
            if os.path.isfile(absolute_file_path) and not os.path.basename(f).startswith('.'):
                root, _ = os.path.splitext(f)
                pkg_list.append(root)
        logger.info("Scan installed package: {}".format(pkg_list))
        return pkg_list
