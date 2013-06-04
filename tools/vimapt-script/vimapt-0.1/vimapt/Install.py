#!/usr/bin/env python

import os
import tempfile
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import re

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

    def init_check(self, package_file):
        self.tmpdir = tempfile.mkdtemp()
        Extract.Extract(package_file, self.tmpdir).extract()

    def check_repeat_install(self):
        self.pkg_name = Vimapt.Vimapt(self.tmpdir).scan_package_name()
        installed_list = Vimapt.Vimapt(self.vim_dir).get_installed_list()
        if self.pkg_name in installed_list:
            msg = "package Name: " + self.pkg_name + " already installed!"
            raise AssertionError(msg)

    def check_depend(self):
        controll_dir = os.path.join(self.tmpdir, "vimapt/control/")
        dir_list = os.listdir(controll_dir)
        if len(dir_list) == 1 and os.path.isfile(dir_list[1]):
            fp = open(dir_list[1])
            file_stream = fp.read()
            fp.close()
            control_data = load(file_stream, Loader=Loader)
            depends_data = control_data["depends"]
            depends_list = depends_data.split(",")
            package_depends_list = []
            for depend in depends_list:
                match = re.match("([\.a-z][a-z0-9]+)\W*\(([^\(\)]+)\)", depend)
                match_list = match.groups()
                if len(match_list) == 0:
                    pass
                else:
                    match_soft = match_list[1]
                    if len(match_list) == 1:
                        match_version = ""
                        match_operater = "*"
                    else:
                        operate = match_list[2]
                        operate_match = re.match("([=><])\W*([0-9\.])+", operate)
                    operate_match_list = operate_match.groups()
                    if len(operate_match_list) == 1:
                        match_operater = "*"
                        match_version = operate_match_list[1]
                    else:
                        match_operater = operate_match_list[1]
                        match_version = operate_match_list[2]
                depend_info = [match_soft, match_operater, match_version] 
                package_depends_list.append(depend_info)
            inner_package_depends_list = {}
            outer_package_depends_list = {}
            for depend in package_depends_list:
                if depend[1].startswith("."):
                    inner_package_depends_list.append(depend)
                else:
                    outer_package_depends_list.append(depend)

            version_dict = Vimapt.Vimapt(self.vim_dir).get_version_dict()
            for depend in inner_package_depends_list:
                if depend[1] in version_dict:
                    if depend[2] != "*":
                        if depend[2] == "=":
                            if depend[3] == version_dict[depend[1]]:
                                continue
                            else:
                                msg = depend[1] + "'s version is " + version_dict[depend[1]] + ", but package want it = " + depend[3]
                                raise AssertionError(msg)
                        elif depend[2] == ">=":
                            if depend[3] >= version_dict[depend[1]]:
                                continue
                            else:
                                msg = depend[1] + "'s version is " + version_dict[depend[1]] + ", but package want it >= " + depend[3]
                                raise AssertionError(msg)
                        elif depend[2] == "<=":
                            if depend[3] <= version_dict[depend[1]]:
                                continue
                            else:
                                msg = depend[1] + "'s version is " + version_dict[depend[1]] + ", but package want it <= " + depend[3]
                                raise AssertionError(msg)
                        elif depend[2] == ">":
                            if depend[3] > version_dict[depend[1]]:
                                continue
                            else:
                                msg = depend[1] + "'s version is " + version_dict[depend[1]] + ", but package want it > " + depend[3]
                                raise AssertionError(msg)
                        elif depend[2] == "<":
                            if depend[3] < version_dict[depend[1]]:
                                continue
                            else:
                                msg = depend[1] + "'s version is " + version_dict[depend[1]] + ", but package want it < " + depend[3]
                                raise AssertionError(msg)
                    else:
                        pass
                else:
                    msg = depend[1] + "is not install!"
                    raise AssertionError(msg)
