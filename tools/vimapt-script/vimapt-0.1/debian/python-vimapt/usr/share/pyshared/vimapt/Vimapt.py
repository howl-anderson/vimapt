#!/usr/bin/env python

import os


class Vimapt:
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def get_installed_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = [f for f in os.listdir(record_dir)
                    if os.path.isfile(os.path.join(record_dir, f))]
        return pkg_list

    def get_presist_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/install')
        pkg_list = [f for f in os.listdir(record_dir)
                    if os.path.isfile(os.path.join(record_dir, f))]
        return pkg_list

    def get_package_list(self):
        pass

    def scan_package_name(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = [f for f in os.listdir(record_dir)
                    if os.path.isfile(os.path.join(record_dir, f))]
        return pkg_list[0]
