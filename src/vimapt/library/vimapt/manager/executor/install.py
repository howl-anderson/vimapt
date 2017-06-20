#!/usr/bin/env python

import logging
import os
import tempfile

import six

from vimapt import LocalRepo
from vimapt import Record
from vimapt.exception import (
    VimaptException,
    VimaptAbortOperationException,
)
from vimapt.hook.constants import (
    HookType,
    HookTypeToMethodNameMapping
)
from vimapt.package_format import get_extractor_by_detect_file

logger = logging.getLogger(__name__)


class VimaptPluginHookNotFound(VimaptException):
    pass


class InstallExecutor(object):
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

    @staticmethod
    def _import_hook_module(package_path, package_name):
        module_file_name = package_name.replace('-', '_')
        module_file_path = os.path.join(package_path, 'vimapt', 'hook', module_file_name + '.py')
        module_name = module_file_name

        if not os.path.exists(module_file_path):
            # hook file not exists, raise exception to stop call chain
            raise VimaptPluginHookNotFound("{} file not exists!".format(module_file_path))

        hook_module = None
        if six.PY2:
            import imp

            hook_module = imp.load_source(module_name, module_file_path)
        else:
            # For python 3.5+
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, module_file_path)
            hook_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hook_module)

        try:
            hook_class = getattr(hook_module, '_VIMAPT_HOOK_CLASS')
        except AttributeError:
            raise VimaptPluginHookNotFound('Can not access `_VIMAPT_HOOK_CLASS` attribute of hook module')
        else:
            return hook_class

    def _init_package_hook(self, package_path, package_name):
        try:
            hook_class = self._import_hook_module(package_path, package_name)
        except VimaptPluginHookNotFound:
            return None
        else:
            hook_instance = hook_class(self.vim_dir, package_path, package_name)
            return hook_instance

    def _run_hook(self, hook_type):
        package_path = self.tmp_dir
        package_name = self.pkg_name

        hook_instance = self._init_package_hook(package_path, package_name)

        if hook_instance is None:
            # hook is not valid in this package, so just return None and finish the process
            return None

        try:
            method_name = HookTypeToMethodNameMapping[hook_type]
        except KeyError as e:
            raise VimaptAbortOperationException(e.message)

        try:
            hook_method = getattr(hook_instance, method_name)
        except AttributeError as e:
            raise VimaptAbortOperationException(e.message)

        try:
            result = hook_method()
        except Exception as e:
            raise VimaptAbortOperationException(e.message)

        if not result:
            raise VimaptAbortOperationException("Hook return a not True, means hook execute failed!")

    def _install_package(self, package_file):
        """
        The real method that install package from local file
        :param package_file: locaton of the package file
        :return: None
        """
        self._init_check(package_file)

        self._run_hook(HookType.PRE_INSTALL)

        extractor = get_extractor_by_detect_file(package_file)
        install = extractor(package_file, self.vim_dir)
        file_list = install.get_file_list()
        install.filter(self._extract_hook)
        install.extract()
        record = Record.Record(self.vim_dir)
        record.install(self.pkg_name, file_list)

        self._run_hook(HookType.POST_INSTALL)

    def file_install(self, package_file):
        """
        Install pckage from local file
        :param package_file: location of package file
        :return: None
        """

        # TODO: disable install from file function for now, but future may open it again

        self._install_package(package_file)

    def repo_install(self, package_name):
        """
        Install package from package repository
        :param package_name: name of the package
        :return: None
        """

        self.pkg_name = package_name

        repo = LocalRepo.LocalRepo(self.vim_dir)
        package_path = repo.get_package(package_name)
        if package_path:
            self._install_package(package_path)
        else:
            raise VimaptAbortOperationException("use network to get repository package error!")

    def execute(self, package_specification):
        logger.info("Start install package {} with vim_dir: {}".format(package_specification, self.vim_dir))

        return self.repo_install(package_specification)

    def _init_check(self, package_file):
        self.tmp_dir = tempfile.mkdtemp()
        extractor = get_extractor_by_detect_file(package_file)
        extractor(package_file, self.tmp_dir).extract()
