import unittest

from depsolver.package \
    import \
        PackageInfo
from depsolver.repository \
    import \
        Repository
from depsolver.version \
    import \
        SemanticVersion

P = PackageInfo.from_string
V = SemanticVersion.from_string

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.numpy_1_6_1 = P("numpy-1.6.1")
        self.numpy_1_7_0 = P("numpy-1.7.0")

        self.scipy_0_11_0 = P("scipy-0.11.0")


    def test_simple_construction(self):
        repo = Repository()
        self.assertEqual(repo.list_packages(), [])

        r_packages = [self.numpy_1_6_1, self.numpy_1_7_0, self.scipy_0_11_0]

        repo = Repository(packages=r_packages)
        packages = set(repo.iter_packages())
        self.assertEqual(packages, set(r_packages))

    def test_has_package(self):
        packages = [self.numpy_1_6_1, self.numpy_1_7_0, self.scipy_0_11_0]
        repo = Repository(packages=packages)

        self.assertTrue(repo.has_package(self.numpy_1_6_1))
        self.assertTrue(repo.has_package_name("numpy"))
        self.assertFalse(repo.has_package_name("floupi"))

    def test_find_package(self):
        packages = [self.numpy_1_6_1, self.numpy_1_7_0, self.scipy_0_11_0]
        repo = Repository(packages=packages)

        self.assertTrue(repo.find_package("numpy", V("1.6.1")))
        self.assertTrue(repo.find_package("numpy", V("1.7.0")))
        self.assertTrue(repo.find_package("numpy", V("1.7.1")) is None)

    def test_add_package(self):
        packages = [self.numpy_1_6_1, self.numpy_1_7_0, self.scipy_0_11_0]

        repo = Repository()
        for package in packages:
            repo.add_package(package)

        self.assertTrue(repo.has_package(self.numpy_1_6_1))
        self.assertTrue(repo.has_package_name("numpy"))
        for package in repo.packages:
            self.assertTrue(package.repository is repo)

    def test_add_package_twice(self):
        repo = Repository([self.numpy_1_6_1])
        self.assertRaises(ValueError, lambda: repo.add_package(self.numpy_1_6_1))

    def test_add_package_multiple_repositories(self):
        repo = Repository([self.numpy_1_6_1])
        self.assertRaises(ValueError, lambda: Repository([self.numpy_1_6_1]))
