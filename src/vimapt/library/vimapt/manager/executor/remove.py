#!/usr/bin/env python

import os
import logging

from vimapt.data_format import loads

logger = logging.getLogger(__name__)


class RemoveExecutor(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def remove_package(self, package_name):
        logger.info("Start to remove package: {}".format(package_name))

        file_path = os.path.join(self.vim_dir,
                                 'vimapt/install',
                                 package_name)
        # print file_path
        fd = open(file_path, 'r')
        file_stream = fd.read()
        fd.close()
        meta_data = loads(file_stream)

        logger.info("Package meta data: {}".format(meta_data))

        for file_name in meta_data:
            target_path = os.path.join(self.vim_dir, file_name)

            # print target_path
            if os.path.isfile(target_path):
                logger.info("Unlink file: {}".format(target_path))
                os.unlink(target_path)
            else:
                pass

        logger.info("Unlink package meta file: {}".format(file_path))
        os.unlink(file_path)

    def execute(self, package_specification):
        logger.info("Start uninstall package {} with vim_dir: {}".format(package_specification, self.vim_dir))

        self.remove_package(package_specification)