#!/usr/bin/env python

import os
import tempfile
import sys
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
        #self.check_premise_of_install(package_file)
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
            #print " get repo package error"
            #TODO
            #sys.exit(1)

    def check_repeat_install(self, package_file):
        self.tmpdir = tempfile.mkdtemp()
        Extract.Extract(package_file, self.tmpdir).extract()
        self.pkg_name = Vimapt.Vimapt(self.tmpdir).scan_package_name()
        installed_list = Vimapt.Vimapt(self.vim_dir).get_installed_list()
        if self.pkg_name in installed_list:
            raise AssertionError("package Name: " + self.pkg_name + " already installed!")
            #print "Package Name: " + self.pkg_name + " already installed!"
            #TODO
            #sys.exit(0)

    def check_premise_of_install(self, package_file):
        premise_dir = os.path.join(self.tmpdir, 'vimapt/premise');
        premise_file = os.path.join(premise_dir, package_file) + ".vim"
        vim.command("source " + premise_file)
        vim.command("let g:vimapt_premise_result = VimAptPremiseOfInstall()")
        vim.command("defunction VimAptPremiseOfInstall")
        premise_result = vim.eval("g:vimapt_premise_result")
        if not premise_result:
            #print "Premise of Install is not meat"
            raise AssertionError("premise of install not meat")
            #TODO
            #sys.exit(0)


if __name__ == "__main__":
    install = Install('/tmp/vim')
    #install.file_install('/home/howl/vcs/howlanderson/vimapt/tools/vimapt-script/vimapt-0.1/vimapt/test.vpb')
    install.repo_install('vimapt-package-example')
