#!/usr/bin/env python

import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def make_vpb(package_file_list, root_dir, output_dir):
    package_data = []
    package_content = []
    for file in package_file_list:
        fd = open(file, 'r')
        file_lines = fd.readlines()
        line_number = len(file_lines)
        package_content += file_lines
        fd.close()
        relfile_path = os.path.relpath(file, root_dir)
        package_data.append([relfile_path, line_number])

    data = {'package':package_data}
    meta_output = dump(data, Dumper=Dumper)
    package_output = "".join(package_content)
    output = meta_output + "\n" + package_output
    output_file = os.path.basename(root_dir) + '.vpb'
    output_file_abspath = os.path.join(output_dir, output_file)
    fd = open(output_file_abspath, 'w')
    fd.write(output)
    fd.close()

def scan_dir(dir_path):
    package_file_list = []
    yid = os.walk(dir_path)
    for root_dir, path_list, file_list in yid:
        for file in file_list:
            print root_dir
            print file
            abspath = os.path.join(root_dir, file)
            print abspath
            package_file_list.append(abspath)
    return package_file_list

def main():
    packaging_path = '/home/howl/vcs/howlanderson/vimapt/src/tools/vimapt/test-0.3'
    package_file_list = scan_dir(packaging_path)
    output_path = os.path.dirname(packaging_path)
    make_vpb(package_file_list, packaging_path, output_path)

if __name__ == "__main__":
    main()
