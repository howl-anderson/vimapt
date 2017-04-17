#!/usr/bin/env python

import os
import re
import tempfile

from .data_format.yaml import load

from . import Record
from . import LocalRepo
from . import Vimapt
from . import Extract


class Install(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir  # user's .vim dir path
        self.pkg_name = None  # package's name
        self.tmp_dir = None

    def extract_hook(self, file_name, _):
        token = file_name.split("/")
        if token[0] == "vimrc":
            file_path = os.path.join(self.vim_dir, file_name)
            if os.path.exists(file_path):
                return False
        else:
            return True

    def install_package(self, package_file):
        self.init_check(package_file)
        self.check_repeat_install()
        self.check_depend()
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
        if package_path:
            self.install_package(package_path)
        else:
            print("use network to get repository package error!")
            raise AssertionError()

    def init_check(self, package_file):
        self.tmp_dir = tempfile.mkdtemp()
        Extract.Extract(package_file, self.tmp_dir).extract()

    def check_repeat_install(self):
        self.pkg_name = Vimapt.Vimapt(self.tmp_dir).scan_package_name()
        installed_list = Vimapt.Vimapt(self.vim_dir).get_installed_list()
        if self.pkg_name in installed_list:
            msg = "package: '" + self.pkg_name + "' already installed!"
            print(msg)
            raise AssertionError()

    def check_depend(self):
        controller_dir = os.path.join(self.tmp_dir, "vimapt/control/")
        dir_list = os.listdir(controller_dir)
        if len(dir_list) == 1 and os.path.isfile(os.path.join(controller_dir, dir_list[0])):
            fp = open(os.path.join(controller_dir, dir_list[0]))
            file_stream = fp.read()
            fp.close()
            control_data = load(file_stream)
            depends_data = control_data["depends"]
            if depends_data == "":
                pass
            else:
                depends_list = depends_data.split(",")
                package_depends_list = []
                for depend in depends_list:
                    match = re.match("\s*([\.a-z][a-z0-9]+)\s*\(\s*([^\(\)]+)\s*\)\s*", depend)
                    if match is None:
                        match = re.match("\s*([\.a-z][a-z0-9]+)\s*", depend)
                        match_list = match.groups()
                    else:
                        match_list = match.groups()

                    if len(match_list) == 0:
                        msg = "package's depend format is broken"
                        print(msg)
                        raise AssertionError()
                    else:
                        match_soft = match_list[0]
                        if len(match_list) == 1:
                            match_version = ""
                            match_operator = "*"
                        else:
                            operate = match_list[1]
                            operate_match = re.match("([=><]+)\s*([0-9\.]+)", operate)
                            operate_match_list = operate_match.groups()
                            if len(operate_match_list) == 1:
                                match_operator = "*"
                                match_version = operate_match_list[0]
                            else:
                                match_operator = operate_match_list[0]
                                match_version = operate_match_list[1]
                    depend_info = [match_soft, match_operator, match_version]
                    package_depends_list.append(depend_info)
                inner_package_depends_list = []
                outer_package_depends_list = []
                for depend in package_depends_list:
                    if depend[0].startswith("."):
                        inner_depend = depend
                        inner_depend[0] = inner_depend[0][1:]
                        inner_package_depends_list.append(depend)
                    else:
                        outer_package_depends_list.append(depend)

                version_dict = Vimapt.Vimapt(self.vim_dir).get_version_dict()
                # TODO:version compare need find a better way
                print(version_dict)
                print(inner_package_depends_list)
                for depend in inner_package_depends_list:
                    if depend[0] in version_dict:
                        if depend[1] != "*":
                            if depend[1] == "=":
                                if version_dict[depend[0]] == depend[2]:
                                    continue
                                else:
                                    msg = "package: " + depend[0] + "'s version is " + version_dict[
                                        depend[0]] + ", but package want it = " + depend[2]
                                    print(msg)
                                    raise AssertionError()
                            elif depend[1] == ">=":
                                if version_dict[depend[0]] >= depend[2]:
                                    continue
                                else:
                                    msg = depend[0] + "'s version is " + version_dict[
                                        depend[0]] + ", but package want it >= " + depend[2]
                                    print(msg)
                                    raise AssertionError()
                            elif depend[1] == "<=":
                                if version_dict[depend[0]] <= depend[2]:
                                    continue
                                else:
                                    msg = depend[0] + "'s version is " + version_dict[
                                        depend[0]] + ", but package want it <= " + depend[2]
                                    print(msg)
                                    raise AssertionError()
                            elif depend[1] == ">":
                                if version_dict[depend[0]] > depend[2]:
                                    continue
                                else:
                                    msg = depend[0] + "'s version is " + version_dict[
                                        depend[0]] + ", but package want it > " + depend[2]
                                    print(msg)
                                    raise AssertionError()
                            elif depend[1] == "<":
                                if version_dict[depend[0]] < depend[2]:
                                    continue
                                else:
                                    msg = depend[0] + "'s version is " + version_dict[
                                        depend[0]] + ", but package want it < " + depend[2]
                                    print(msg)
                                    raise AssertionError()
                        else:
                            pass
                    else:
                        msg = "inner depend package '" + depend[0] + "' is not install!"
                        print(msg)
                        raise AssertionError()
        else:
            msg = "package format is broken"
            print(msg)
            raise AssertionError()