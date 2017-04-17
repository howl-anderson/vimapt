#!/usr/bin/env python

import logging
import os

from yaml import Loader
from yaml import load

from .RepositoryConfigParser import RepositoryConfigParser

logger = logging.getLogger(__file__)


class TransporterBase(RepositoryConfigParser):
    def __init__(self, dispatcher, dot_vim_dir):
        self.DISPATCHER = dispatcher
        self.DOT_VIM_DIR = dot_vim_dir

        # basic path setting
        self.CACHE_DIR = os.path.join(self.DOT_VIM_DIR, 'vimapt/cache')

        self.CACHE_POOL_DIR = os.path.join(self.CACHE_DIR, 'pool')
        self.LOCAL_PACKAGE_INDEX_FILE = os.path.join(self.CACHE_DIR, 'index/package')
        self.REMOTE_PACKAGE_INDEX_RELATIVE_PATH = 'index/package'

        # load config
        self.LOCAL_PACKAGE_INDEX = self.load_local_package_index(self.LOCAL_PACKAGE_INDEX_FILE)

    def get_package(self, package_name):
        if not self.check_package_in_repository(package_name):
            logger.info("Package %s not in repository", package_name)
            print("Package %s not in repository", package_name)
            return None

        return self.fetch_package(package_name)

    def fetch_package(self, package_name):
        raise NotImplementedError

    def get_index(self):
        return self.fetch_index()

    def fetch_index(self):
        raise NotImplementedError

    def write_package_to_cache_pool(self, package_stream, package_full_name):
        local_package_path = os.path.join(self.CACHE_POOL_DIR, package_full_name)

        fd = open(local_package_path, 'w')
        fd.write(package_stream)
        fd.close()

        return local_package_path

    def check_package_in_repository(self, package_name):
        if package_name not in self.LOCAL_PACKAGE_INDEX:
            return False

    @staticmethod
    def load_local_package_index(local_package_index_file):
        fd = open(local_package_index_file)
        source_stream = fd.read()
        fd.close()
        source_data = load(source_stream, Loader=Loader)
        return source_data

    def get_package_relative_path(self, package_name):
        package_relative_path = self.LOCAL_PACKAGE_INDEX[package_name]['path']
        return package_relative_path

    def write_local_package_index(self, stream):
        fd = open(self.LOCAL_PACKAGE_INDEX_FILE, 'w')
        fd.write(stream)
        fd.close()
