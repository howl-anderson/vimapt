import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from depsolver.debian_version \
    import \
        DebianVersion, is_valid_debian_version

V = DebianVersion.from_string

class TestVersionParsing(unittest.TestCase):
    def test_valid_versions(self):
        versions = ["1.2.0", "1.2.3-1", "0:1.2.3-1"]

        for version in versions:
            self.assertTrue(is_valid_debian_version(version))

    def test_roundtrip(self):
        versions = ["1.2.0", "1.2.0-0", "0:1.2.0"]

        for version in versions:
            self.assertEqual(str(V(version)), version)

class TestVersionComparison(unittest.TestCase):
    def test_eq(self):
        self.assertTrue(V("1.2.3") == V("1.2.3"))
        self.assertTrue(V("1.2.3") == V("0:1.2.3"))
        self.assertTrue(V("1.2.3") == V("1.2.3-0"))
        self.assertFalse(V("1.2.3") == V("1:1.2.3"))

    def test_lt(self):
        self.assertTrue(V("1") < V("2"))
        self.assertTrue(V("1.0") < V("1.1"))
        self.assertTrue(V("1.0") < V("1:1.0"))
        self.assertTrue(V("1.0") < V("1.0-1"))
        self.assertTrue(V("1.0-1bpo1") < V("1.0-1.1"))

    def test_gt(self):
        self.assertTrue(V("2") > V("1"))
        self.assertTrue(V("1.2.3") > V("1.2.1"))
        self.assertTrue(V("1.0-1") > V("1.0-0"))
        self.assertTrue(V("1.0-1") > V("1.0-0.1"))
        self.assertTrue(V("1.0beta1") > V("1.0"))
        self.assertTrue(V("1.0beta1") > V("1.0-1"))
        self.assertTrue(V("1.0-1bpo1") > V("1.0-1"))
        self.assertTrue(V("1.0-1") > V("1.0-1~sarge1"))
