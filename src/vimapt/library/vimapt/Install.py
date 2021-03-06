#!/usr/bin/env python

import os
import tempfile
import logging

import requirements
import semantic_version

from .data_format import loads
from vimapt.exception import VimaptAbortOperationException
from . import Record
from . import LocalRepo
from . import Vimapt
from . import Extract

logger = logging.getLogger(__name__)


class Install(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir  # user's .vim dir path
        self.pkg_name = None  # package's name
        self.tmp_dir = None

    def _extract_hook(self, file_name, _):
        """
        Installer filter object: if *.vimrc file exists in the system, new *.vimrc file will not overwrite it.
        :param file_name: name of the file
        :param _: stream of the file, just ignore it
        :return: Boolean, False means not extract this file to system, so keep the old config file alive.
        """
        token = file_name.split("/")
        if token[0] == "vimrc":
            file_path = os.path.join(self.vim_dir, file_name)
            if os.path.exists(file_path):
                logger.info("<%s> keep local version, developer's version is not overwrite.", file_name)
                return False
        return True

    def _install_package(self, package_file):
        """
        The real method that install package from local file
        :param package_file: locaton of the package file
        :return: None
        """
        self._init_check(package_file)
        self._check_repeat_install()
        self._check_depend()
        install = Extract.Extract(package_file, self.vim_dir)
        file_list = install.get_file_list()
        install.filter(self._extract_hook)
        install.extract()
        record = Record.Record(self.vim_dir)
        record.install(self.pkg_name, file_list)

    def file_install(self, package_file):
        """
        Install pckage from local file
        :param package_file: location of package file
        :return: None
        """
        self._install_package(package_file)

    def repo_install(self, package_name):
        """
        Install package from package repository
        :param package_name: name of the package
        :return: None
        """
        repo = LocalRepo.LocalRepo(self.vim_dir)
        package_path = repo.get_package(package_name)
        if package_path:
            self._install_package(package_path)
        else:
            raise VimaptAbortOperationException("use network to get repository package error!")

    def _init_check(self, package_file):
        self.tmp_dir = tempfile.mkdtemp()
        Extract.Extract(package_file, self.tmp_dir).extract()

    def _check_repeat_install(self):
        """
        Check if same package name has been installed
        :return: None
        """
        self.pkg_name = Vimapt.Vimapt(self.tmp_dir).scan_package_name()
        installed_list = Vimapt.Vimapt(self.vim_dir).get_installed_list()
        if self.pkg_name in installed_list:
            msg = "package: '" + self.pkg_name + "' already installed!"
            raise VimaptAbortOperationException(msg)

    def _check_depend(self):
        """
        Check if all the requirements is meet
        :return: None
        """
        controller_dir = os.path.join(self.tmp_dir, "vimapt/control/")
        dir_list = os.listdir(controller_dir)
        controller_file = os.path.join(controller_dir, dir_list[0])

        with open(controller_file) as fp:
            file_stream = fp.read()

        control_data = loads(file_stream) or dict()  # in case control file is empty

        logger.info("<%s> control data: %s", controller_file, control_data)

        depends_data = control_data.get("depends", [])
        conflicts_data = control_data.get("conflicts", [])

        depend_items = self._parse_requirement(depends_data)
        conflicts_items = self._parse_requirement(conflicts_data)

        logger.info("<%s> depend data: %s", controller_file, depend_items)
        logger.info("<%s> conflicts data: %s", controller_file, conflicts_items)

        _, not_matched_requirements = self._check_requirement(depend_items)
        matched_requirements, _ = self._check_requirement(conflicts_items)

        if not len(not_matched_requirements) and not len(matched_requirements):
            logger.info("<%s> check depend is pass!", controller_file)
            return True

        msg = ("package requirements is not meet,"
               " fellow dependency: %s is not meet,"
               " or fellow conflicted package: %s already installed")
        raise VimaptAbortOperationException(msg % (not_matched_requirements, matched_requirements))

    def _parse_requirement(self, requirements_data):
        """
        parse the requirement data
        
        :param requirements_data: list of string or string
        :return: list of requirements object
        """
        requirements_items = []

        # if requirement is a string, then translate to a single element list
        if isinstance(requirements_data, str):
            requirements_data = [requirements_data]

        for requirement_str in requirements_data:
            requirements_items.extend(list(requirements.parse(requirement_str)))
        return requirements_items

    def _check_requirement(self, requirements):
        """
        get list of packages installed or not installed
        :param requirements: list of package specification
        :return: a tuple: (list of packages installed, list of packages not installed)
        """
        not_matched_requirements = []
        matched_requirements = []

        version_dict = Vimapt.Vimapt(self.vim_dir).get_version_dict()

        for requirement in requirements:
            try:
                package_version = version_dict[requirement.name]
            except KeyError:
                not_matched_requirements.append(requirement)
                continue

            check_pass_flag = True

            installed_version = semantic_version.Version(package_version)

            for spec_requirement in requirement.specs:
                version_comparer = self._get_comparer(spec_requirement[0])
                require_version = semantic_version.Version(spec_requirement[1])
                if not version_comparer(installed_version, require_version):
                    not_matched_requirements.append(requirement)
                    check_pass_flag = False
                    break

            if check_pass_flag:
                matched_requirements.append(requirement)

        return matched_requirements, not_matched_requirements

    def _get_comparer(self, comparer_str):
        """
        Get comparer object by comparer string
        :param comparer_str: string represent the compare operator
        :return: An executable object that take two arguments and return boolean
        """
        mapping = {
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y
        }

        try:
            comparer = mapping[comparer_str]
        except KeyError:
            raise ValueError("No such comparer %s" % comparer_str)

        return comparer