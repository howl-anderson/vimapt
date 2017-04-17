#!/usr/bin/env python

import os

from .data_format import loads


class Remove(object):
    def __init__(self, package_name, vim_dir):
        self.vim_dir = vim_dir
        self.package_name = package_name

    def remove_package(self):
        file_path = os.path.join(self.vim_dir,
                                 'vimapt/install',
                                 self.package_name)
        # print file_path
        fd = open(file_path, 'r')
        file_stream = fd.read()
        fd.close()
        meta_data = loads(file_stream)

        for file_name, _ in meta_data:
            file_token = file_name.split("/")
            if file_token[0] == "vimrc":
                continue
            target_path = os.path.join(self.vim_dir, file_name)

            # print target_path
            if os.path.isfile(target_path):
                os.unlink(target_path)
            else:
                pass
        remove_path = os.path.join(self.vim_dir,
                                   'vimapt/remove',
                                   self.package_name)
        os.rename(file_path, remove_path)
