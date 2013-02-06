#!/usr/bin/env python

import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Remove():
    def __init__(self, package_name, vim_dir):
        self.vim_dir = vim_dir
        self.package_name = package_name

    def remove_package(self):
        file_path = os.path.join(self.vim_dir, 'vimapt/install', self.package_name)
        fd = open(file_path, 'r')
        file_stream = fd.read()
        fd.close()
        meta_data = load(file_stream, Loader=Loader)

        for file, _ in meta_data:
            file_token = file.split("/")
            if file_token[0] == "vimrc":
                continue
            target_path = os.path.join(self.vim_dir, file) 
            if os.path.isfile(target_path):
                os.unlink(target_path)
            else:
                pass
        remove_path = os.path.join(self.vim_dir, 'vimapt/remove', self.package_name)
        os.rename(file_path, remove_path)
