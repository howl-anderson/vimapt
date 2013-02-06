#!/usr/bin/env python

import urllib
import os
from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


class RemoteRepo(object):
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

    def make_package_index(self):
        pool_reldir = "pool"
        package_relpath = "index/package"
        self.pool_absdir = os.path.join(self.repo_dir, pool_reldir)
        self.package_abspath = os.path.join(self.repo_dir, package_relpath)
        package_data = self.scan_pool()
        package_stream = dump(package_data, Dumper=Dumper)
        fd = open(self.package_abspath, 'w')
        fd.write(package_stream)
        fd.close()

    def scan_pool(self):
        files = [f for f in os.listdir(self.pool_absdir)
                 if os.path.isfile(os.path.join(self.pool_absdir, f))]
        package_data = {}
        for file in files:
            package_name, version_and_ext = file.split('_', 1)
            version = os.path.splitext(version_and_ext)[0]
            path = os.path.join('pool/', file)
            package_info = {'version': version, 'path': path}
            package_data[package_name] = package_info
        return package_data


def main():
    current_dir = os.getcwd()
    repo = RemoteRepo(current_dir)
    repo.make_package_index()

if __name__ == "__main__":
    main()
