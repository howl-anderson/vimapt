#!/usr/bin/env python

import os
from . import makevpb


def make_pool(work_dir):
    for (dir_path, dir_names, file_names) in os.walk(work_dir):
        for dir_name in dir_names:
            pkg_dir = os.path.join(dir_path, dir_name)
            obj = makevpb.VimAptMakeVpb(pkg_dir)
            try:
                obj.make()
            except Exception as e:
                print("%s build failed!" % dir_name)
                print(e)
            else:
                print("%s build successful!" % dir_name)
        break


def main():
    make_pool(os.getcwd())

if __name__ == "__main__":
    main()
