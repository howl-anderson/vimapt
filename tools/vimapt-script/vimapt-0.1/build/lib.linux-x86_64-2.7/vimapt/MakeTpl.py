#!/usr/bin/env python

import os
import sys
import shutil
from . import Extract
import errno


class MakeTpl():
    def __init__(self, work_dir):
        self.tpl_file = 'tpl.vpb'
        self.work_dir = work_dir

    def make_tpl(self):
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        tpl_absfile = os.path.join(current_file_dir, self.tpl_file)
        package_name = raw_input("Input you package name:\n")
        prompt_message = "Input you package version. Format like x.y.z:\n"
        package_version = raw_input(prompt_message)
        print package_name
        print package_version
        package_dir = package_name + '-' + package_version
        package_dir_abspath = os.path.join(self.work_dir, package_dir)
        if os.path.isdir(package_dir_abspath):
            prompt_message = "Target dir: \"" + package_dir_abspath + "\" exists, should i remove it? (y,N):\n"
            rm_exists_dir = raw_input(prompt_message)
            if rm_exists_dir == "y":
                shutil.rmtree(package_dir_abspath)
                print "Target dir remove successed!"
            else:
                print "Target exists and user choice to aborted, exit!"
                sys.exit(0)
        extract_object = Extract.Extract(tpl_absfile, package_dir_abspath)
        extract_object.extract()
        print "New packaging dir build in: \"", package_dir_abspath, "\""
        package_control_path = os.path.join(package_dir_abspath, 'vimapt/control')
        package_copyright_path = os.path.join(package_dir_abspath, 'vimapt/copyright')

        tpl_control_file = os.path.join(package_control_path, 'vimapt')
        target_control_file = os.path.join(package_control_path, package_name)
        os.rename(tpl_control_file, target_control_file)

        tpl_copyright_file = os.path.join(package_copyright_path, 'vimapt')
        target_copyright_file = os.path.join(package_copyright_path, package_name)
        os.rename(tpl_copyright_file, target_copyright_file)
        print "Every thing done! Tpl making is successed!"
        print "Have fun!"


def main():
    work_dir = os.getcwd()
    make_tpl_object = MakeTpl(work_dir)
    make_tpl_object.make_tpl()

if __name__ == "__main__":
    main()
