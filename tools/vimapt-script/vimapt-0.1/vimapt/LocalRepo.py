#!/usr/bin/env python

import urllib
import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class LocalRepo(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir
        self.config_path = os.path.join(self.vim_dir, 'vimapt/source')
        self.cache_dir = os.path.join(self.vim_dir, 'vimapt/cache')
        self.cache_pool_dir = os.path.join(self.cache_dir, 'pool')
        self.local_package_index_path = os.path.join(self.cache_dir,
                                                     'index/package')
        self.remote_package_index_relpath = 'index/package'

    def get_remote_package_index(self, source_url):
        filehandle = urllib.urlopen(source_url)
        source_stream = filehandle.read()
        return source_stream

    def write_local_package_index(self, stream):
        fd = open(self.local_package_index_path, 'w')
        fd.write(stream)
        fd.close()

    def get_config(self):
        fd = open(self.config_path)
        source_stream = fd.read()
        fd.close()
        return source_stream.strip()

    def update(self):
        source_server = self.get_config()
        remote_source_url = os.path.join(source_server,
                                         self.remote_package_index_relpath)
        source_stream = self.get_remote_package_index(remote_source_url)
        self.write_local_package_index(source_stream)

    def extract(self):
        fd = open(self.local_package_index_path)
        source_stream = fd.read()
        fd.close()
        source_data = load(source_stream, Loader=Loader)
        return source_data

    def get_package(self, package_name):
        source_data = self.extract()
        if not package_name in source_data:
            print "NOT FOUND package: " + package_name
            return False
        else:
            package_relpath = source_data[package_name]['path']
            source_server = self.get_config()
            package_url = os.path.join(source_server, package_relpath)

            filehandle = urllib.urlopen(package_url) # TODO: add proxy and timeout
            package_stream = filehandle.read()
            package_full_name = os.path.basename(package_url)
            local_package_path = os.path.join(self.cache_pool_dir,
                                              package_full_name)

            fd = open(local_package_path, 'w')
            fd.write(package_stream)
            fd.close()
            return local_package_path
