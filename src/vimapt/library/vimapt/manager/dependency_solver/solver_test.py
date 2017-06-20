import unittest

import mock
from depsolver import PackageInfo
from depsolver.solver.operations import Install

from vimapt.manager.dependency_solver import DependencySolver


class SolverTest(unittest.TestCase):
    def test_main(self):
        solver = DependencySolver(None)

        solver.get_installed_package_list = mock.MagicMock(return_value=[])

        repository_package_list = [
            {
                'name': 'pkg',
                'version': '1.0.0',
                'depends': '',
                'conflicts': ''
            },
        ]
        solver.get_repository_package_list = mock.MagicMock(return_value=repository_package_list)

        operation_list = solver.solve('pkg')

        self.assertEqual(len(operation_list), 1)
        self.assertTrue(isinstance(operation_list[0], Install))
        self.assertEqual(str(operation_list[0].package), str(PackageInfo.from_string('pkg-1.0.0')))

    def test_already_install_package(self):
        solver = DependencySolver(None)

        installed_package_list = [
            {
                'name': 'pkg',
                'version': '1.0.0',
                'depends': '',
                'conflicts': ''
            },
        ]

        solver.get_installed_package_list = mock.MagicMock(return_value=installed_package_list)

        solver.get_repository_package_list = mock.MagicMock(return_value=installed_package_list)

        operation_list = solver.solve('pkg')

        self.assertEqual(len(operation_list), 0)

    def test_conflict_install_package(self):
        solver = DependencySolver(None)

        installed_package_list = [
            {
                'name': 'pkg',
                'version': '1.0.0',
                'depends': '',
                'conflicts': ''
            },
        ]

        solver.get_installed_package_list = mock.MagicMock(return_value=installed_package_list)

        repository_package_list = [
            {
                'name': 'antpkg',
                'version': '1.0.0',
                'depends': '',
                'conflicts': 'pkg'
            },
        ]
        solver.get_repository_package_list = mock.MagicMock(return_value=repository_package_list)

        operation_list = solver.solve('antpkg')

        self.assertEqual(len(operation_list), 0)
