#!/usr/bin/env python

import os
import tempfile
from . import Record
from . import LocalRepo
from . import Vimapt
from . import Extract


class Install():
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir
        self.pkg_name = None
        self.tmpdir = None

    def extract_hook(self, file, _):
        token = file.split("/")
        if token[0] == "vimrc":
            file_path = os.path.join(self.vim_dir, file)
            if os.path.exists(file_path):
                return False
        else:
            return True

    def install_package(self, package_file):
        self.check_repeat_install(package_file)
        install = Extract.Extract(package_file, self.vim_dir)
        file_list = install.get_file_list()
        install.filter(self.extract_hook)
        install.extract()
        record = Record.Record(self.pkg_name, self.vim_dir)
        record.install(file_list)

    def file_install(self, package_file):
        self.install_package(package_file)

    def repo_install(self, package_name):
        repo = LocalRepo.LocalRepo(self.vim_dir)
        package_path = repo.get_package(package_name)
        #print package_path
        if package_path:
            self.install_package(package_path)
        else:
            raise AssertionError("get repo package error")

    def check_repeat_install(self, package_file):
        self.tmpdir = tempfile.mkdtemp()
        Extract.Extract(package_file, self.tmpdir).extract()
        self.pkg_name = Vimapt.Vimapt(self.tmpdir).scan_package_name()
        installed_list = Vimapt.Vimapt(self.vim_dir).get_installed_list()
        if self.pkg_name in installed_list:
            msg = "package Name: " + self.pkg_name + " already installed!"
            raise AssertionError(msg)
