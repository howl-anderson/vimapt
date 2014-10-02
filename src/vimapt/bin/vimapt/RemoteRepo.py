#!/usr/bin/env python

import os
from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


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
        package_stream = dump(package_data, Dumper=Dumper)
        fd = open(self.package_abspath, 'w')
        fd.write(package_stream)
        fd.close()

    def scan_pool(self):
        files = [f for f in os.listdir(self.pool_absolute_dir)
                 if os.path.isfile(os.path.join(self.pool_absolute_dir, f))]
        package_data = {}
        for file_name in files:
            package_name, version_and_ext = file_name.split('_', 1)
            version = os.path.splitext(version_and_ext)[0]
            path = os.path.join('pool/', file_name)
            package_info = {'version': version, 'path': path}
            package_data[package_name] = package_info
        return package_data