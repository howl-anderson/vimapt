#!/usr/bin/env python

import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Purge():
    def __init__(self, package_name, vim_dir):
        self.vim_dir = vim_dir
        self.package_name = package_name

    def purge_package(self):
        file_install_path = os.path.join(self.vim_dir, 'vimapt/install', self.package_name)
        file_reomve_path = os.path.join(self.vim_dir, 'vimapt/remove', self.package_name)
        if os.path.isfile(file_install_path):
            file_path = file_install_path
        else:
            file_path = file_reomve_path
        fd = open(file_path, 'r')
        file_stream = fd.read()
        fd.close()
        meta_data = load(file_stream, Loader=Loader)
        
        for file, _ in meta_data:
            target_path = os.path.join(self.vim_dir, file) 
            if os.path.isfile(target_path):
                os.unlink(target_path)
            else:
                pass
        os.unlink(file_path)
