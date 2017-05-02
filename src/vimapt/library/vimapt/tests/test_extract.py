import unittest

from vimapt.Extract import Extract


class TestExtract(unittest.TestCase):
    def test_main(self):
        o = Extract("vimapt_1.0-1.vpb", "./output")
        o.extract()
