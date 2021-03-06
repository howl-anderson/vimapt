#!/usr/bin/env python

import os

from vimapt import Compress


class VimAptMakeVpb(object):
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.target_dir = os.path.dirname(self.work_dir)
        self.dir_name = os.path.basename(self.work_dir)

        # initial setup
        pkg_name_segments = self.dir_name.split("_")
        self.pkg_name = '_'.join(pkg_name_segments[:-1])
        full_version = pkg_name_segments[-1]

        self.full_pkg_name = self.pkg_name + "_" + full_version + ".vpb"
        self.target_file = os.path.join(self.target_dir, self.full_pkg_name)

    def make(self):
        compress_object = Compress.Compress(self.work_dir, self.target_file)
        compress_object.compress()


def main():
    obj = VimAptMakeVpb(os.getcwd())
    obj.make()

if __name__ == "__main__":
    main()
