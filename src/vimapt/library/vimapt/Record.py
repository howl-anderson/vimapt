#!/usr/bin/env python

import os

from .data_format import dump


class Record:
    def __init__(self, package_name, output_dir):
        self.output_dir = output_dir
        self.package_name = package_name

    def install(self, meta_data):
        record_dir = os.path.join(self.output_dir, "vimapt/install")
        record_file = os.path.join(record_dir, self.package_name)
        fd = open(record_file, 'w')
        meta_stream = dump(meta_data)
        fd.write(meta_stream)
        fd.close()
