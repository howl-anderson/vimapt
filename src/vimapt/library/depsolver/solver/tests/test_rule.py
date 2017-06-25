import unittest

from depsolver.package \
    import \
        PackageInfo
from depsolver.pool \
    import \
        Pool
from depsolver.repository \
    import \
        Repository
from depsolver.solver.rule \
    import \
        PackageRule

P = PackageInfo.from_string

class TestPackageRule(unittest.TestCase):
    def test_ctor_simple(self):
        repository = Repository([P("mkl-10.1.0"),
                                 P("numpy-1.7.0; depends (MKL >= 10.1.0)"),
                                 P("scipy-0.12.0; depends (numpy >= 1.7.0)")])
        pool = Pool([repository])

        rule = PackageRule(pool, [1, 2], "job_install", "scipy")

        self.assertEqual(rule.enabled, True)
        self.assertEqual(rule.literals, [1, 2])
        self.assertEqual(rule.reason, "job_install")
        self.assertEqual(rule.rule_hash, "05cf2")

    def test_from_packages_simple(self):
        mkl = P("mkl-10.1.0")
        numpy = P("numpy-1.7.0; depends (MKL >= 10.1.0)")
        scipy = P("scipy-0.12.0; depends (numpy >= 1.7.0)")
        remote_repository = [mkl, numpy, scipy]

        i_mkl = P("mkl-10.1.0")
        installed_repository = [i_mkl]

        pool = Pool([Repository(remote_repository), Repository(installed_repository)])

        rule = PackageRule.from_packages(pool, [mkl, i_mkl], "job_install", "numpy")

        self.assertEqual(rule.enabled, True)
        self.assertEqual(rule.literals, [mkl.id, i_mkl.id])
        self.assertEqual(rule.reason, "job_install")

    def test_str_simple(self):
        repository = Repository([P("mkl-10.1.0"),
                                 P("numpy-1.7.0; depends (MKL >= 10.1.0)"),
                                 P("scipy-0.12.0; depends (numpy >= 1.7.0)")])
        pool = Pool([repository])

        rule = PackageRule(pool, [1, 2], "job_install", "scipy")

        self.assertEqual(str(rule), "(+mkl-10.1.0 | +numpy-1.7.0)")

        rule = PackageRule(pool, [-1, 2], "job_install", "scipy")

        self.assertEqual(str(rule), "(-mkl-10.1.0 | +numpy-1.7.0)")
