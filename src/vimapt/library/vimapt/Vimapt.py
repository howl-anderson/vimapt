#!/usr/bin/env python

import os
import logging

from .data_format import loads

logger = logging.getLogger(__name__)


class Vimapt(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def get_installed_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)
        return pkg_list

    def get_version_dict(self):
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
                control_data = loads(file_stream)
                version = control_data["version"]
                root, ext = os.path.splitext(f)
                version_dict[root] = version

                logger.info("get result <%s>", (root, version))

        return version_dict

    # TODO: function name need do something
    def get_presist_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/install')
        pkg_list = []

        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                pkg_list.append(f)

        return pkg_list

    def get_package_list(self):
        pass

    def scan_package_name(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)) and not os.path.basename(f).startswith('.'):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)

        return pkg_list[0]
