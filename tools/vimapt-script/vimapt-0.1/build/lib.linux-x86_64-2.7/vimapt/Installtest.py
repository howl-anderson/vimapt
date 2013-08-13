#!/usr/bin/env python

import unittest

import Install

class DefaultWidgetSizeTestCase(unittest.TestCase):
    def runTest(self): 
        install = Install.Install("./vim")
        install.install_package("./vimapt_1.0-1.vpb")

if __name__ == "__main__":
    DefaultWidgetSizeTestCase().runTest()
