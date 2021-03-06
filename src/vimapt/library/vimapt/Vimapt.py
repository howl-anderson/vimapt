#!/usr/bin/env python

import os
import logging

from .data_format import loads

logger = logging.getLogger(__name__)


class Vimapt(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def get_installed_list(self):
        """
        Get installed packages list by scan 'vimapt/control' directory
        :return: List of package names
        """
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)
        return pkg_list

    def get_version_dict(self):
        """
        Get installed package name-version dict by scan 'vimapt/control' directory
        :return: Dict of package-version mapping, e.g. {'pkg1': 'version-string', 'pkg2': 'other-version-string'}
        """
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        version_dict = {}
        for f in os.listdir(record_dir):
            f_abspath = os.path.join(record_dir, f)

            # ignore hidden file or directory
            if os.path.basename(f_abspath).startswith('.'):
                continue

            if os.path.isfile(f_abspath):

                logger.info("scan control info on <%s>", f_abspath)

                fd = open(f_abspath)
                file_stream = fd.read()
                fd.close()
                control_data = loads(file_stream) or dict()
                version = control_data.get("version")
                root, ext = os.path.splitext(f)
                version_dict[root] = version

                logger.info("get result <%s>", (root, version))

        return version_dict

    # TODO: function name need do something
    def get_presist_list(self):
        """
        Get package name list by scan 'vimapt/install' directory
        :return: List of package names
        """
        record_dir = os.path.join(self.vim_dir, 'vimapt/install')
        pkg_list = []

        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                pkg_list.append(f)

        return pkg_list

    def get_package_list(self):
        pass

    def scan_package_name(self):
        """
        Get package name by scan 'vimapt/control', used to discover the package's name only
        :return: String of package name
        """
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)

        return pkg_list[0]
