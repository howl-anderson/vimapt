#!/usr/bin/env python

import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Vimapt:
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def get_installed_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)
        return pkg_list

    def get_version_dict(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        version_dict = {}
        for f in os.listdir(record_dir):
            f_abspath = os.path.join(record_dir, f)
            if os.path.isfile(f_abspath):
                fd = open(f_abspath)
                file_stream = fd.read()
                fd.close()
                control_data = load(file_stream, Loader=Loader)
                version = control_data["version"]
                root, ext = os.path.splitext(f)
                version_dict[root] = version
        return version_dict

    # TODO: function name need do something
    def get_presist_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/install')
        pkg_list = [f for f in os.listdir(record_dir)
                    if os.path.isfile(os.path.join(record_dir, f))]
        return pkg_list

    def get_package_list(self):
        pass

    def scan_package_name(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            if os.path.isfile(os.path.join(record_dir, f)):
                root, ext = os.path.splitext(f)
                pkg_list.append(root)
        return pkg_list[0]