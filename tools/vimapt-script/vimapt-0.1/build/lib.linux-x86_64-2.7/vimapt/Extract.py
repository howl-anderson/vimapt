#!/usr/bin/env python

import os
import tempfile
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Extract():
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

    def extract(self):
        fd = open(self.input_file, 'r')
        file_stream = fd.read()
        fd.close()
        meta_stream, package_stream = file_stream.split('\n\n', 1)
        meta_data = load(meta_stream, Loader=Loader)
        package_lines = package_stream.split('\n')
        package_data = {}
        start_point = 0
        for file, filelines in meta_data['package']:
            print file, filelines
            print start_point
            end_point = start_point + filelines
            list_data = package_lines[start_point:end_point]
            file_stream = "\n".join(list_data)
            package_data[file] = file_stream
            package_dir = os.path.dirname(file)
            package_absdir = os.path.join(self.output_dir, package_dir)
            package_abspath_file = os.path.join(self.output_dir, file)
            if not os.path.isdir(package_absdir):
                os.makedirs(package_absdir)
            fd = open(package_abspath_file, 'w')
            fd.write(file_stream)
            fd.close()
            start_point += filelines


def main():
    input_file = 'test-0.3.vpb'
    #output_dir = tempfile.mkdtemp()
    output_dir = 'testdir'
    extract(input_file, output_dir)
    #plugin_name = get_plugin_name(input_file)
    #check_depends(tmp_dir, plugin_name)

if __name__ == "__main__":
    main()
