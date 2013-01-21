#!/usr/bin/env python

import urllib
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class RemoteRepo(object):
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
    
    def make_package_index(self):
        base_dir = self.repo_dir
        pool_reldir = "pool"
        package_relpath = "index/package"
        pool_absdir = os.path.join(base_dir, pool_reldir)
        package_abspath = os.path.join(base_dir, package_relpath)
        package_data = self.scan_pool(pool_absdir)
        package_stream = dump(package_data, Dumper=Dumper)
        fd = open(package_abspath, 'w')
        fd.write(package_stream)
        fd.close()
    
    
    def scan_pool(self, pool_dir):
        files = [f for f in os.listdir(pool_dir) if os.path.isfile(os.path.join(pool_dir, f))]
        package_data = {}
        for file in files:
            package_name, version_and_ext = file.split('-', 1)
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
