#!/usr/bin/env python

import os
import tempfile
import logging

from .data_format import dumps, loads
from vimapt.exception import (
    VimaptException,
    VimaptAbortOperationException,
)
from vimapt.package_format import get_extractor_by_detect_file

logger = logging.getLogger(__name__)


class RemoteRepo(object):
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

        # initial setup
        pool_relative_dir = "pool"
        package_relative_path = "index/package"
        self.pool_absolute_dir = os.path.join(self.repo_dir, pool_relative_dir)
        self.package_abspath = os.path.join(self.repo_dir, package_relative_path)

    def make_package_index(self):
        package_data = self.scan_pool()
        package_stream = dumps(package_data)
        fd = open(self.package_abspath, 'w')
        fd.write(package_stream)
        fd.close()

    def scan_pool(self):
        files = [f for f in os.listdir(self.pool_absolute_dir)
                 if os.path.isfile(os.path.join(self.pool_absolute_dir, f))]
        package_data = {}
        for file_name in files:
            pkg_name_segments = file_name.split("_")
            package_name = '_'.join(pkg_name_segments[:-1])
            version_and_ext = pkg_name_segments[-1]

            package_absolute_path = os.path.join(self.pool_absolute_dir, file_name)
            meta_data = self.read_package_meta_data_by_file(package_absolute_path)

            version = os.path.splitext(version_and_ext)[0]
            path = os.path.join('pool/', file_name)
            package_info = {
                'version': version,
                'path': path,
                'depends': meta_data.get('depends', ''),
                'conflicts': meta_data.get('conflicts', '')
            }
            package_data[package_name] = package_info
        return package_data

    def read_package_meta_data_by_dir(self, package_dir_path):
        """
        Get package name by scan 'vimapt/control', used to discover the package's name only
        :return: String of package name
        """
        record_dir = os.path.join(package_dir_path, 'vimapt/control')
        meta_file_list = []
        meta_data = None
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                meta_file_list.append(f)
                with open(os.path.join(record_dir, f)) as fd:
                    meta_data = loads(fd.read())

        if len(meta_file_list) != 1:
            msg = ("Can not read package meta data: "
                   "There are not only one meta file, "
                   "there are {} meta files: {}.").format(len(meta_file_list), meta_file_list)
            raise VimaptAbortOperationException(msg)

        return meta_data

    def read_package_meta_data_by_file(self, package_file):
        logger.info("Start to process {}".format(package_file))

        tmp_dir = tempfile.mkdtemp()

        extractor = get_extractor_by_detect_file(package_file)
        install = extractor(package_file, tmp_dir)
        install.extract()

        return self.read_package_meta_data_by_dir(tmp_dir)
