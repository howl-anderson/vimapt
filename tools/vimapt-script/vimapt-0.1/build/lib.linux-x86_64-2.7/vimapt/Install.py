#!/usr/bin/env python

import os
import sys
from . import LocalRepo
from . import Extract


class Install():
    def __init__(self, vim_dir, package_name):
        self.vim_dir = vim_dir
        self.package_name = package_name

    def install_package(self):
        repo = LocalRepo.LocalRepo(self.vim_dir)
        repo.update()
        package_path = repo.get_package(self.package_name)
        #print package_path
        install = Extract.Extract(package_path, vim_dir)
        install.extract()


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    install = Install(vim_dir, package_name)
    install.install_package()

if __name__ == "__main__":
    main()
