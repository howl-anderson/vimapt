#!/usr/bin/env python

import os

from .data_format import dumps


class Record:
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def install(self, package_name, meta_data):
        record_dir = os.path.join(self.vim_dir, "vimapt/install")
        record_file = os.path.join(record_dir, package_name)
        fd = open(record_file, 'w')
        meta_stream = dumps(meta_data)
        fd.write(meta_stream)
        fd.close()
