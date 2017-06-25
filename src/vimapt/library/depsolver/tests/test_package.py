import hashlib
import unittest

import six

from depsolver.errors \
    import \
        DepSolverError
from depsolver.package \
    import \
        PackageInfo, parse_package_full_name
from depsolver.repository \
    import \
        Repository
from depsolver.requirement \
    import \
        Requirement
from depsolver.version \
    import \
        SemanticVersion

V = SemanticVersion.from_string
R = Requirement.from_string

class TestPackageInfo(unittest.TestCase):
    def test_simple_construction(self):
        r_provides = []

        package = PackageInfo("numpy", V("1.3.0"))
        self.assertEqual(package.provides, r_provides)
        self.assertEqual(package.dependencies, [])
        self.assertEqual(package.id, -1)

        r_provides = [R("numpy == 1.3.0")]
        r_id = -1

        package = PackageInfo("nomkl_numpy", V("1.3.0"), provides=r_provides)
        self.assertEqual(package.provides, r_provides)
        self.assertEqual(package.id, r_id)

    def test_construction(self):
        r_provides = []

        package = PackageInfo(name="numpy", version=V("1.3.0"))
        self.assertEqual(package.provides, r_provides)
        self.assertEqual(package.dependencies, [])
        self.assertEqual(package.id, -1)

        r_provides = [R("numpy == 1.3.0")]
        r_id = -1

        package = PackageInfo(name="nomkl_numpy", version=V("1.3.0"), provides=r_provides)
        self.assertEqual(package.provides, r_provides)
        self.assertEqual(package.id, r_id)

    def test_unique_name(self):
        package = PackageInfo(name="numpy", version=V("1.3.0"))
        self.assertEqual(package.unique_name, "numpy-1.3.0")

    def test_str(self):
        provides = [R("numpy == 1.3.0")]
        package = PackageInfo(name="nomkl_numpy", version=V("1.3.0"), provides=provides)
        self.assertEqual(str(package), "nomkl_numpy-1.3.0")

    def test_repr(self):
        package = PackageInfo(name="numpy", version=V("1.3.0"))
        if six.PY3:
            self.assertEqual(repr(package), "PackageInfo('numpy-1.3.0')")
        else:
            self.assertEqual(repr(package), "PackageInfo(u'numpy-1.3.0')")

        package = PackageInfo(name="numpy", version=V("1.6.0"), dependencies=[R("mkl >= 10.3.0")])
        if six.PY3:
            self.assertEqual(repr(package), "PackageInfo('numpy-1.6.0; depends (mkl >= 10.3.0)')")
        else:
            self.assertEqual(repr(package), "PackageInfo(u'numpy-1.6.0; depends (mkl >= 10.3.0)')")

    def test_set_repository(self):
        package = PackageInfo(name="numpy", version=V("1.3.0"))
        package.repository = Repository()

        def set_repository():
            package.repository = Repository()
        self.assertRaises(ValueError, set_repository)

class TestPackageInfoFromString(unittest.TestCase):
    def test_simple(self):
        r_package_string = "numpy-1.3.0"
        r_package = PackageInfo(name="numpy", version=V("1.3.0"))

        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)
        self.assertRaises(DepSolverError, lambda: PackageInfo.from_string("numpy 1.3.0"))

    def test_dependencies(self):
        r_package_string = "numpy-1.6.0; depends (mkl >= 10.3.0)"
        r_package = PackageInfo(name="numpy", version=V("1.6.0"), dependencies=[R("mkl >= 10.3.0")])
        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

    def test_provides(self):
        r_package_string = "nomkl_numpy-1.6.0; provides (numpy == 1.6.0)"
        r_package = PackageInfo(name="nomkl_numpy", version=V("1.6.0"), provides=[R("numpy == 1.6.0")])
        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

    def test_conflicts(self):
        r_package_string = "nomkl_numpy-1.6.0; conflicts (numpy == 1.6.0)"
        r_package = PackageInfo(name="nomkl_numpy", version=V("1.6.0"),
                                conflicts=[R("numpy == 1.6.0")])

        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

    def test_replaces(self):
        r_package_string = "mkl_numpy-1.6.0; replaces (numpy == 1.6.0)"
        r_package = PackageInfo(name="mkl_numpy", version=V("1.6.0"), replaces=[R("numpy == 1.6.0")])
        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

    def test_suggests(self):
        r_package_string = "numpy-1.6.0; suggests (scipy == 1.6.0)"
        r_package = PackageInfo(name="numpy", version=V("1.6.0"), suggests=[R("scipy")])

        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

class TestParsePackageName(unittest.TestCase):
    def test_multiple_dependencies(self):
        r_package_string = "scipy-0.12.0; depends (numpy >= 1.6.0, " \
                           "numpy < 1.7.0, MKL >= 10.3.0, MKL < 10.4.0)"
        r_package = PackageInfo(name="scipy", version=V("0.12.0"),
                                dependencies=[R("numpy >= 1.6.0, numpy < 1.7.0"),
                                              R("MKL >= 10.3.0, MKL < 10.4.0")])

        package = PackageInfo.from_string(r_package_string)

        self.assertEqual(package, r_package)
        self.assertEqual(package.package_string, r_package_string)

    def test_simple(self):
        name, version = parse_package_full_name("numpy-1.6.0")
        self.assertEqual(name, "numpy")
        self.assertEqual(version, "1.6.0")
