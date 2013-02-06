#!/usr/bin/env python

import os
from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

class Record:
    def __init__(self, package_name, output_dir):
        self.output_dir = output_dir
        self.package_name = package_name

    def install(self, meta_data):
        record_dir = os.path.join(self.output_dir,  "vimapt/install")
        record_file = os.path.join(record_dir, self.package_name)
        fd = open(record_file, 'w')
        meta_stream = dump(meta_data, Dumper=Dumper)
        fd.write(meta_stream)
        fd.close()
