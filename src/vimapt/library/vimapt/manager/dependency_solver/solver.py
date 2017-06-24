# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os

from depsolver import PackageInfo, Pool, Repository, Request, Requirement, Solver

from vimapt import LocalRepo
from vimapt.data_format import loads
from vimapt.manager.manage_action import ManageAction

logger = logging.getLogger(__name__)


class DependencySolver(object):
    action_mapping = {
        ManageAction.INSTALL: 'install',
        ManageAction.UNINSTALL: 'remove',
        ManageAction.UPDATE: 'update'
    }

    def __init__(self, vim_dir):
        self.vim_dir = vim_dir
        self.pkg_name = None  # package's name

    def solve(self, action, package_specification):
        logger.info("Start to scan repository packages.")

        repository_package_list = []
        for package_data in self.get_repository_package_list():
            package_info_string = '; '.join([
                '{}-{}'.format(package_data['name'], package_data['version']),
                'depends ({})'.format(package_data['depends']),
                'conflicts ({})'.format(package_data['conflicts'])
            ])

            logger.info("Scanned package: {}".format(package_info_string))

            package_info = PackageInfo.from_string(package_info_string)
            repository_package_list.append(package_info)

        logger.info("End of scanning repository packages.")

        repo = Repository(repository_package_list)

        installed_package_list = []

        logger.info("Start to scan installed packages.")

        for package_data in self.get_installed_package_list():
            package_info_string = '; '.join([
                '{}-{}'.format(package_data['name'], package_data['version']),
                'depends ({})'.format(package_data['depends']),
                'conflicts ({})'.format(package_data['conflicts'])
            ])

            logger.info("Scanned package: {}".format(package_info_string))

            package_info = PackageInfo.from_string(package_info_string)
            installed_package_list.append(package_info)

        logger.info("End of scanning installed packages.")

        installed_repo = Repository(installed_package_list)
        pool = Pool([repo, installed_repo])

        request = Request(pool)

        request_action = getattr(request, self.action_mapping[action])
        request_action(Requirement.from_string(package_specification))

        # request.install(Requirement.from_string(package_specification))

        operation_list = Solver(pool, installed_repo).solve(request)
        return operation_list

    def get_installed_package_list(self):
        record_dir = os.path.join(self.vim_dir, 'vimapt/control')
        pkg_list = []
        for f in os.listdir(record_dir):
            absolute_file_path = os.path.join(record_dir, f)
            if os.path.isfile(absolute_file_path) and not os.path.basename(f).startswith('.'):
                root, ext = os.path.splitext(f)
                with open(absolute_file_path) as fd:
                    meta_data = loads(fd.read())
                pkg_list.append({
                    'name': root,
                    'version': meta_data.get('version'),
                    'depends': meta_data.get('depends', ''),
                    'conflicts': meta_data.get('conflicts', '')
                })
        return pkg_list

    def get_repository_package_list(self):
        package_list = []
        for package_name, package_data in LocalRepo.LocalRepo(self.vim_dir).get_local_package_repository().items():
            package_info = package_data
            package_info['name'] = package_name
            package_list.append(package_info)

        return package_list