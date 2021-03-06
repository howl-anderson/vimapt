#!/usr/bin/env python

import os
import contextlib

import six
import six.moves.urllib.request as urllib_request

from .data_format import loads


class LocalRepo(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir
        self.config_path = os.path.join(self.vim_dir, 'vimapt/source')
        self.cache_dir = os.path.join(self.vim_dir, 'vimapt/cache')
        self.cache_pool_dir = os.path.join(self.cache_dir, 'pool')
        self.local_package_index_path = os.path.join(self.cache_dir,
                                                     'index/package')
        self.remote_package_index_relative_path = 'index/package'

    def _get_remote_package_index(self, source_url):
        """
        Get package repository's index content
        :param source_url: URL of repository's index
        :return: string, content of index
        """
        fd = urllib_request.urlopen(source_url)
        source_stream = fd.read()
        fd.close()

        if six.PY2:
            return source_stream
        else:
            return source_stream.decode('utf-8')

    def _write_local_package_index(self, stream):
        """
        Write repository's index to local repository cache
        :param stream: content of index
        :return: None
        """
        fd = open(self.local_package_index_path, 'w')
        fd.write(stream)
        fd.close()

    def _get_config(self):
        """
        read package source URL
        :return: string, URL of package repository
        """
        fd = open(self.config_path)
        source_stream = fd.read()
        fd.close()
        return source_stream.strip()

    def update(self):
        """
        Update local repository's index from remote index
        :return: 
        """
        source_server = self._get_config()
        remote_source_url = os.path.join(source_server,
                                         self.remote_package_index_relative_path)
        source_stream = self._get_remote_package_index(remote_source_url)
        self._write_local_package_index(source_stream)

    def _extract(self):
        """
        Load local repository's index
        :return: Dict, repository's index
        """
        fd = open(self.local_package_index_path)
        source_stream = fd.read()
        fd.close()
        source_data = loads(source_stream)
        return source_data

    def get_package(self, package_name):
        """
        Get package by name from remote repository
        :param package_name: name of package
        :return: local path of package file
        """
        source_data = self._extract()
        if package_name not in source_data:
            print("Not found package: " + package_name)
            return False
        else:
            package_relative_path = source_data[package_name]['path']
            source_server = self._get_config()
            package_url = os.path.join(source_server, package_relative_path)

            with contextlib.closing(urllib_request.urlopen(package_url)) as fd:  # TODO: add proxy and timeout, may use requests library
                package_stream = fd.read()

            if six.PY3:
                package_stream = package_stream.decode('utf-8')

            package_full_name = os.path.basename(package_url)
            local_package_path = os.path.join(self.cache_pool_dir,
                                              package_full_name)

            fd = open(local_package_path, 'w')
            fd.write(package_stream)
            fd.close()
            return local_package_path
