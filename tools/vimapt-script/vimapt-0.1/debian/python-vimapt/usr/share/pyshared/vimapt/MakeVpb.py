#!/usr/bin/env python

import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class MakeVpb():
    def __init__(self, package_path, output_path):
        self.package_path = package_path
        self.output_path = output_path

    def make_vpb(self):
        package_file_list = self.scan_dir()
        package_data = []
        package_content = []
        for file in package_file_list:
            fd = open(file, 'r')
            file_lines = fd.readlines()
            line_number = len(file_lines)
            #if is not empty file
            if line_number:
                last_line = file_lines[-1]
                if not last_line.endswith("\n"):
                    file_lines[-1] += "\n"
                package_content += file_lines
            fd.close()
            relfile_path = os.path.relpath(file, self.package_path)
            package_data.append([relfile_path, line_number])

        data = {'package': package_data}
        meta_output = dump(data, Dumper=Dumper)
        package_output = "".join(package_content)
        output = meta_output + "\n" + package_output
        dir_name = os.path.basename(self.package_path)
        pkg_fullname = self.dir2pkgname(dir_name)
        output_file = pkg_fullname + '.vpb'
        output_file_abspath = os.path.join(self.output_path, output_file)
        fd = open(output_file_abspath, 'w')
        fd.write(output)
        fd.close()

    def dir2pkgname(self, dir_name):
        dir_token = dir_name.split('-')
        version = dir_token[-1] 
        pkg_name_token = dir_token[:-1]
        pkg_name = "-".join(pkg_name_token)
        pkg_fullname = pkg_name + "_" + version
        return pkg_fullname

    def scan_dir(self):
        package_file_list = []
        yid = os.walk(self.package_path)
        for root_dir, path_list, file_list in yid:
            for file in file_list:
                #print root_dir
                #print file
                abspath = os.path.join(root_dir, file)
                #print abspath
                package_file_list.append(abspath)
        return package_file_list


def main():
    #TODO should check the target dir is a well formart
    #dir name and good struct
    packaging_path = os.getcwd()
    #packaging_path =
    #'/home/how/vcs/howlanderson/vimapt/src/tools/vimapt/test-0.3'
    package_file_list = scan_dir(packaging_path)
    output_path = os.path.dirname(packaging_path)
    make_vpb(package_file_list, packaging_path, output_path)

if __name__ == "__main__":
    main()
