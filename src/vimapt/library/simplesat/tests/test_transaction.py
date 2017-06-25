#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import unittest
from textwrap import dedent

from simplesat.test_utils import pool_and_repository_from_packages

from ..transaction import (
    InstallOperation, RemoveOperation, Transaction, UpdateOperation
)


PACKAGE_DEF = dedent("""\
    A 0.0.0-1; depends (C ^= 0.0.0)
    A 3.0.0-1; depends (G ^= 1.0.0)
    B 0.0.0-1; depends (D ^= 0.0.0)
    B 1.0.0-1
    C 0.0.0-1
    D 0.0.0-1
    E 0.0.0-1; depends (A ^= 0.0.0)
    E 1.0.0-1; depends (I ^= 0.0.0, B ^= 1.0.0)
    F 0.0.0-1
    G 1.0.0-1
    I 0.0.0-1; depends (J ^= 0.0.0)
    J 0.0.0-1
    X 0.0.0-1; depends (A ^= 0.0.0, B ^= 0.0.0)
    X 1.0.0-1; depends (A ^= 3.0.0, B ^= 1.0.0)
    Y 0.0.0-1; depends (X ^= 0.0.0)
    Y 1.0.0-1
    Y 2.0.0-1; depends (F ^= 0.0.0)
    Y 3.0.0-1; depends (X ^= 1.0.0)
    Z 0.0.0-1; depends (E ^= 0.0.0)
    Z 1.0.0-1; depends (E ^= 1.0.0)
""")


class TestTransaction(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.pool, self.repo = pool_and_repository_from_packages(PACKAGE_DEF)

    def test_operations(self):

        # Given
        installed = {1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 19}
        wanted = {20, 8, 11, 12, 4}
        decisions = wanted.union(-i for i in installed if i not in wanted)
        to_install = (4, 8, 20)
        to_remove = (19, 15, 13, 7, 3, 1, 10, 9, 6, 5)

        # When
        installs = [InstallOperation(self.pool.id_to_package(i))
                    for i in to_install]
        removals = [RemoveOperation(self.pool.id_to_package(i))
                    for i in to_remove]
        transaction = Transaction(self.pool, decisions, installed)
        result = transaction.operations
        expected = removals + installs

        # Then
        self.assertListEqual(expected, result)

    def test_pretty_operations(self):

        # Given
        installed = {1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15}
        wanted = {20, 8, 11, 12, 4}
        decisions = wanted.union(-i for i in installed if i not in wanted)
        to_install = (20,)
        to_update = ((3, 4), (7, 8))
        to_remove = (15, 13, 1, 10, 9, 6, 5)

        # When
        installs = [InstallOperation(self.pool.id_to_package(i))
                    for i in to_install]
        updates = [UpdateOperation(self.pool.id_to_package(new),
                                   self.pool.id_to_package(old))
                   for old, new in to_update]
        removals = [RemoveOperation(self.pool.id_to_package(i))
                    for i in to_remove]
        transaction = Transaction(self.pool, decisions, installed)
        result = transaction.pretty_operations
        expected = removals + updates + installs

        # Then
        self.assertListEqual(expected, result)
