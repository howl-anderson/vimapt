import six

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

from depsolver.package \
    import \
        PackageInfo
from depsolver.pool \
    import \
        Pool
from depsolver.repository \
    import \
        Repository
from depsolver.requirement \
    import \
        Requirement

from depsolver.solver.core \
    import \
        Install, Solver, Update
from depsolver.solver.policy \
    import \
        DefaultPolicy

R = Requirement.from_string

mkl_10_1_0 = PackageInfo.from_string("mkl-10.1.0")
mkl_10_2_0 = PackageInfo.from_string("mkl-10.2.0")
mkl_10_3_0 = PackageInfo.from_string("mkl-10.3.0")
mkl_11_0_0 = PackageInfo.from_string("mkl-11.0.0")

numpy_1_6_0 = PackageInfo.from_string("numpy-1.6.0; depends (mkl)")
numpy_1_6_1 = PackageInfo.from_string("numpy-1.6.1; depends (mkl)")
numpy_1_7_0 = PackageInfo.from_string("numpy-1.7.0; depends (mkl)")

nomkl_numpy_1_7_0 = PackageInfo.from_string("nomkl_numpy-1.7.0; depends (numpy == 1.7.0)")

scipy_0_10_1 = PackageInfo.from_string("scipy-0.10.1; depends (numpy >= 1.6.0)")
scipy_0_11_0 = PackageInfo.from_string("scipy-0.11.0; depends (numpy >= 1.6.0)")
scipy_0_12_0 = PackageInfo.from_string("scipy-0.12.0; depends (numpy >= 1.7.0)")

policy = DefaultPolicy()

def solve(pool, requirement, installed_repository, policy):
    solver = Solver(pool, installed_repository, policy)
    return solver.solve(requirement)

class TestSimpleScenario(unittest.TestCase):
    """Scenario with no dependencies."""
    @unittest.expectedFailure
    def test_no_install(self):
        """Ensure the most up-to-date version is installed when directly installed."""
        repo = Repository([mkl_10_1_0, mkl_10_2_0, mkl_10_3_0, mkl_11_0_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()

        operations = solve(pool, R("mkl"), installed_repo, policy)
        self.assertEqual(operations, [Install(mkl_11_0_0)])

    @unittest.expectedFailure
    def test_already_satisfied(self):
        """Ensure we don't install a more recent version when the requirement
        is already satisfied."""
        repo = Repository([mkl_10_1_0, mkl_10_2_0, mkl_10_3_0, mkl_11_0_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()
        installed_repo.add_package(mkl_10_2_0)

        operations = solve(pool, R("mkl"), installed_repo, policy)
        self.assertEqual(operations, [])

    @unittest.expectedFailure
    def test_already_installed_but_not_satisfied(self):
        """Ensure we update to the most recent version when the requirement
        is not already satisfied."""
        repo = Repository([mkl_10_1_0, mkl_10_2_0, mkl_10_3_0, mkl_11_0_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()
        installed_repo.add_package(mkl_10_2_0)

        operations = solve(pool, R("mkl >= 10.3.0"), installed_repo, policy)
        self.assertEqual(operations, [Update(mkl_10_2_0, mkl_11_0_0)])

class TestOneLevel(unittest.TestCase):
    """Scenario with one level of dependencies."""
    @unittest.expectedFailure
    def test_simple(self):
        """Numpy depends on MKL, one version of NumPy only."""
        repo = Repository([mkl_10_2_0, mkl_10_3_0, mkl_11_0_0, numpy_1_6_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()

        operations = solve(pool, R("numpy"), installed_repo, policy)
        self.assertEqual(operations, [Install(mkl_11_0_0), Install(numpy_1_6_0)])

    @unittest.expectedFailure
    def test_simple2(self):
        """Numpy depends on MKL, ensure we install the most up-to-date version."""
        repo = Repository([mkl_10_2_0, mkl_10_3_0, mkl_11_0_0, numpy_1_6_0, numpy_1_7_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()

        operations = solve(pool, R("numpy"), installed_repo, policy)
        self.assertEqual(operations, [Install(mkl_11_0_0), Install(numpy_1_7_0)])

    @unittest.expectedFailure
    def test_dependency_already_provided(self):
        """Numpy depends on MKL, MKL already installed."""
        repo = Repository([mkl_10_2_0, mkl_10_3_0, mkl_11_0_0, numpy_1_6_0, numpy_1_7_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository([mkl_11_0_0])

        operations = solve(pool, R("numpy"), installed_repo, policy)
        self.assertEqual(operations, [Install(numpy_1_7_0)])

    @unittest.expectedFailure
    def test_dependency_already_provided_but_older(self):
        """Numpy depends on MKL, older MKL already installed."""
        repo = Repository([mkl_10_2_0, mkl_10_3_0, mkl_11_0_0, numpy_1_6_0, numpy_1_7_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository([mkl_10_3_0])

        operations = solve(pool, R("numpy"), installed_repo, policy)
        self.assertEqual(operations, [Install(numpy_1_7_0)])

class TestTwoLevels(unittest.TestCase):
    """Scenario with one level of dependencies."""
    @unittest.expectedFailure
    def test_simple(self):
        r_operations = [Install(mkl_11_0_0), Install(numpy_1_7_0),
                Install(scipy_0_12_0)]

        repo = Repository([mkl_10_3_0, mkl_11_0_0, numpy_1_6_0, numpy_1_6_1,
                           numpy_1_7_0, scipy_0_12_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()

        req = R("scipy")

        operations = solve(pool, req, installed_repo, policy)
        self.assertEqual(operations, r_operations)

    @unittest.expectedFailure
    def test_simple_provided(self):
        r_operations = [Install(nomkl_numpy_1_7_0), Install(scipy_0_11_0)]
        repo = Repository([mkl_11_0_0, scipy_0_11_0, nomkl_numpy_1_7_0])

        pool = Pool()
        pool.add_repository(repo)

        installed_repo = Repository()

        operations = solve(pool, R("scipy"), installed_repo, policy)
        self.assertEqual(operations, r_operations)
