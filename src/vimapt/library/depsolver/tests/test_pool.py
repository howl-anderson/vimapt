import unittest

from depsolver.errors \
    import \
        DepSolverError, MissingPackageInfoInPool

from depsolver.package \
    import \
        PackageInfo
from depsolver.pool \
    import \
        MATCH, MATCH_NAME, MATCH_PROVIDE, Pool
from depsolver.repository \
    import \
        Repository
from depsolver.requirement \
    import \
        Requirement

P = PackageInfo.from_string
R = Requirement.from_string

class TestPool(unittest.TestCase):
    def setUp(self):
        self.mkl_10_1_0 = P("mkl-10.1.0")
        self.mkl_10_2_0 = P("mkl-10.2.0")
        self.mkl_10_3_0 = P("mkl-10.3.0")
        self.mkl_11_0_0 = P("mkl-11.0.0")

        self.numpy_1_6_0 = P("numpy-1.6.0; depends (mkl)")
        self.numpy_1_6_1 = P("numpy-1.6.1; depends (mkl)")
        self.numpy_1_7_0 = P("numpy-1.7.0; depends (mkl >= 11.0.0)")

        self.nomkl_numpy_1_7_0 = P("nomkl_numpy-1.7.0; depends (numpy == 1.7.0); provides (numpy == 1.7.0)")

    def test_simple(self):
        r_id = [1, 2]

        repo1 = Repository(packages=[self.mkl_10_1_0, self.mkl_10_2_0])
        pool = Pool()
        pool.add_repository(repo1)

        self.assertEqual(self.mkl_10_1_0.id, r_id[0])
        self.assertEqual(self.mkl_10_2_0.id, r_id[1])

        self.assertRaises(MissingPackageInfoInPool, lambda: pool.package_by_id(self.mkl_10_3_0.id))

    def test_package_by_id_simple(self):
        repo = Repository([self.mkl_10_1_0, self.mkl_10_2_0])
        pool = Pool()
        pool.add_repository(repo)

        self.assertEqual(self.mkl_10_1_0, pool.package_by_id(self.mkl_10_1_0.id))
        self.assertEqual(self.mkl_10_2_0, pool.package_by_id(self.mkl_10_2_0.id))

    def test_simple2(self):
        repo = Repository([self.mkl_10_1_0, self.mkl_10_2_0])
        pool = Pool([repo])

        self.assertEqual(self.mkl_10_1_0, pool.package_by_id(self.mkl_10_1_0.id))
        self.assertEqual(self.mkl_10_2_0, pool.package_by_id(self.mkl_10_2_0.id))
        self.assertRaises(MissingPackageInfoInPool, lambda: pool.package_by_id(self.mkl_10_3_0.id))

    def test_literal_to_string(self):
        pool = Pool([Repository([self.mkl_10_1_0, self.mkl_10_2_0])])

        self.assertEqual(pool.id_to_string(self.mkl_10_2_0.id),
                         "+mkl-10.2.0")
        self.assertEqual(pool.id_to_string(-self.mkl_10_1_0.id),
                         "-mkl-10.1.0")

    def test_has_package(self):
        pool = Pool([Repository([self.mkl_10_1_0, self.mkl_10_2_0])])

        self.assertTrue(pool.has_package(self.mkl_10_1_0))
        self.assertFalse(pool.has_package(self.mkl_11_0_0))

    def test_add_repository(self):
        """Ensures we do not add the same package twice."""
        repo1 = Repository([self.mkl_10_1_0, self.mkl_10_2_0])
        pool = Pool()
        pool.add_repository(repo1)

        repo2 = Repository([P(str(self.mkl_10_1_0))])
        pool.add_repository(repo2)

        self.assertEqual(len(pool.what_provides(R("mkl"))), 3)

    def test_matches(self):
        pool = Pool()

        self.assertEqual(pool.matches(self.mkl_10_1_0, R("mkl")), MATCH)
        self.assertEqual(pool.matches(self.mkl_10_1_0, R("mkl >= 10.2.0")), MATCH_NAME)
        self.assertEqual(pool.matches(self.mkl_10_1_0, R("numpy")), False)
        self.assertEqual(pool.matches(self.nomkl_numpy_1_7_0, R("numpy")), MATCH_PROVIDE)

    def test_what_provides_simple(self):
        repo1 = Repository([self.numpy_1_6_0, self.numpy_1_7_0])
        pool = Pool()
        pool.add_repository(repo1)

        self.assertEqual(set(pool.what_provides(R("numpy"))), set([self.numpy_1_6_0, self.numpy_1_7_0]))
        self.assertEqual(pool.what_provides(R("numpy >= 1.6.1")), [self.numpy_1_7_0])

        repo1 = Repository([self.nomkl_numpy_1_7_0])
        pool = Pool()
        pool.add_repository(repo1)

        self.assertEqual(pool.what_provides(R("numpy")), [self.nomkl_numpy_1_7_0])

    def test_what_provides_direct_only(self):
        repo1 = Repository([self.nomkl_numpy_1_7_0])
        pool = Pool()
        pool.add_repository(repo1)

        self.assertEqual(set(pool.what_provides(R("numpy"))), set([self.nomkl_numpy_1_7_0]))

    def test_what_provides_include_indirect(self):
        repo1 = Repository([self.numpy_1_6_0, self.numpy_1_7_0, self.nomkl_numpy_1_7_0])
        pool = Pool()
        pool.add_repository(repo1)

        self.assertEqual(pool.what_provides(R("numpy >= 1.6.1")), [self.numpy_1_7_0])
        self.assertEqual(set(pool.what_provides(R("numpy"), 'include_indirect')),
                         set([self.numpy_1_6_0, self.numpy_1_7_0, self.nomkl_numpy_1_7_0]))
        self.assertEqual(set(pool.what_provides(R("numpy >= 1.6.1"), 'include_indirect')),
                         set([self.numpy_1_7_0, self.nomkl_numpy_1_7_0]))
        self.assertEqual(set(pool.what_provides(R("numpy >= 1.6.1"), 'direct_only')),
                         set([self.numpy_1_7_0]))

    def test_what_provides_replaces(self):
        scikit_learn = P("scikit_learn-0.12.0")
        sklearn = P("sklearn-0.13.0; replaces (scikit_learn==0.12.0)")
        pool = Pool([Repository([scikit_learn, sklearn])])

        self.assertEqual(set(pool.what_provides(R("sklearn"))), set([sklearn]))
        self.assertEqual(set(pool.what_provides(R("scikit_learn"))), set([sklearn, scikit_learn]))

    def test_priority_simple(self):
        paid_repo = Repository([
            self.mkl_10_1_0,
            self.mkl_10_2_0,
            self.mkl_10_3_0,
            self.mkl_11_0_0,
            self.numpy_1_6_0,
            self.numpy_1_7_0,
        ], name="paid")
        free_repo = Repository([self.nomkl_numpy_1_7_0], "free")
        pool = Pool([paid_repo, free_repo])
        pool.set_repository_order("free", before="paid")

        self.assertEqual(pool.repository_priority(paid_repo), 0)
        self.assertEqual(pool.repository_priority(free_repo), -1)

    def test_priority_not_registered(self):
        repo = Repository()
        pool = Pool()

        self.assertRaises(DepSolverError, lambda: pool.repository_priority(repo))
        self.assertRaises(DepSolverError, lambda: pool.set_repository_order(repo, "dummy"))

    def test_priority_no_name(self):
        paid_repo = Repository([
            self.mkl_10_1_0,
            self.mkl_10_2_0,
            self.mkl_10_3_0,
            self.mkl_11_0_0,
            self.numpy_1_7_0,
        ], name="paid")
        free_repo = Repository([self.nomkl_numpy_1_7_0], "free")
        another_repo = Repository([self.numpy_1_6_1], "another_repo")
        another_repo_wo_name = Repository([self.numpy_1_6_0])
        pool = Pool([paid_repo, free_repo, another_repo, another_repo_wo_name])
        pool.set_repository_order("free", before="paid")

        self.assertEqual(pool.repository_priority(paid_repo), 0)
        self.assertEqual(pool.repository_priority(free_repo), -1)
        self.assertEqual(pool.repository_priority(another_repo), -1)
        self.assertEqual(pool.repository_priority(another_repo_wo_name), -1)
