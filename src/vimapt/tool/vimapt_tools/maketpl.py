#!/usr/bin/env python

import os
import sys

from six.moves import input

from vimapt import Extract


class Make(object):
    def __init__(self, work_dir):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.tpl_file = os.path.join(current_file_dir, 'data', 'vimapt.vpb')
        self.work_dir = work_dir

    def manual_make(self):
        package_name = input("Input you package name:\n")
        prompt_message = "Input you package version. Format like x.y.z:\n"
        package_version = input(prompt_message)
        package_dir = package_name + '_' + package_version
        package_dir_abspath = os.path.join(self.work_dir, package_dir)
        if os.path.isdir(package_dir_abspath):
            print("Target dir exists, exit!")
            sys.exit(0)
        else:
            os.mkdir(package_dir_abspath)
        extract_object = Extract.Extract(self.tpl_file, package_dir_abspath)
        extract_object.extract()
        print("New packaging directory build in: %s" % package_dir_abspath)

        rel_tpl_list = ['vimapt/control/vimapt.yaml',
                        'vimapt/copyright/vimapt.yaml',
                        'vimrc/vimapt.vimrc',
                        ]

        for rel_tpl_file in rel_tpl_list:
            tpl_file = os.path.join(package_dir_abspath, rel_tpl_file)
            tpl_file_dir = os.path.dirname(tpl_file)
            _, ext_name = os.path.splitext(tpl_file)
            target_file = os.path.join(tpl_file_dir, package_name + ext_name)
            print(tpl_file)
            print(target_file)
            os.rename(tpl_file, target_file)

        print("Jobs done! Template making is succeed!")
        print("Have fun!")

    def auto_make(self, package_name, package_version, package_revision):
        tpl_abs_file = self.tpl_file
        full_version = package_version + '-' + package_revision
        package_dir = package_name + '_' + full_version
        package_dir_abspath = os.path.join(self.work_dir, package_dir)
        if os.path.isdir(package_dir_abspath):
            print("Target dir exists, exit!")
            sys.exit(0)
        else:
            os.mkdir(package_dir_abspath)
        extract_object = Extract.Extract(tpl_abs_file, package_dir_abspath)
        extract_object.extract()
        rel_tpl_list = ['vimapt/control/vimapt.yaml',
                        'vimapt/copyright/vimapt.yaml',
                        'vimrc/vimapt.vimrc',
                        ]

        for rel_tpl_file in rel_tpl_list:
            tpl_file = os.path.join(package_dir_abspath, rel_tpl_file)
            tpl_file_dir = os.path.dirname(tpl_file)
            _, ext_name = os.path.splitext(tpl_file)
            target_file = os.path.join(tpl_file_dir, package_name + ext_name)
            print(tpl_file)
            print(target_file)
            os.rename(tpl_file, target_file)


def main():
    current_dir = os.getcwd()
    make = Make(current_dir)
    make.manual_make()

if __name__ == "__main__":
    main()
