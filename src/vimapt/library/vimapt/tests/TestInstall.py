import unittest

from vimapt.Install import Install


class TestInstall(unittest.TestCase):
    def test_main(self):
        install = Install("./vim")
        install.install_package("./vimapt_1.0-1.vpb")
