#!/usr/bin/env python

import os
import logging
import urllib
import urlparse

from .TransporterBase import TransporterBase

logger = logging.getLogger(__file__)


class HttpTransporterBase(TransporterBase):
    def fetch_package(self, package_name):
        self.check_scheme()

        package_relative_path = self.get_package_relative_path(package_name)
        source_server_uri = self.DISPATCHER.REPOSITORY_CONFIG.geturl()
        package_url = urlparse.urljoin(source_server_uri, package_relative_path)

        fd = urllib.urlopen(package_url)  # TODO: add proxy and timeout, may use requests library
        package_stream = fd.read()
        fd.close()
        package_full_name = os.path.basename(package_url)

        local_package_path = self.write_package_to_cache_pool(package_stream, package_full_name)
        return local_package_path

    def check_scheme(self):
        if self.DISPATCHER.REPOSITORY_CONFIG.scheme.lower() != 'http':
            logger.error("%s can not handle scheme '%s'", self.__class__, self.DISPATCHER.REPOSITORY_CONFIG.scheme)
            raise RuntimeError("%s can not handle scheme '%s'", self.__class__, self.DISPATCHER.REPOSITORY_CONFIG.scheme)

    def fetch_index(self):
        source_server = self.DISPATCHER.REPOSITORY_CONFIG.geturl()
        remote_source_url = urlparse.urljoin(source_server, self.REMOTE_PACKAGE_INDEX_RELATIVE_PATH)
        fd = urllib.urlopen(remote_source_url)
        source_stream = fd.read()
        fd.close()
        self.write_local_package_index(source_stream)
