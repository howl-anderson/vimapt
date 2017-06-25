import six

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

from depsolver.errors \
    import \
        DepSolverError, UndefinedDecision
from depsolver.package \
    import \
        PackageInfo
from depsolver.pool \
    import \
        Pool
from depsolver.repository \
    import \
        Repository
from depsolver.solver.decisions \
    import \
        DecisionsSet

P = PackageInfo.from_string

class TestDecisionsSet(unittest.TestCase):
    def setUp(self):
        self.mkl_10_1_0 = P("mkl-10.1.0")
        self.mkl_10_2_0 = P("mkl-10.2.0")
        self.mkl_10_3_0 = P("mkl-10.3.0")
        self.mkl_11_0_0 = P("mkl-11.0.0")

        self.numpy_1_6_1 = P("numpy-1.6.1; depends (mkl)")
        self.numpy_1_7_0 = P("numpy-1.7.0; depends (mkl)")

        repository = Repository([self.mkl_10_1_0, self.mkl_10_2_0,
            self.mkl_10_3_0, self.mkl_11_0_0, self.numpy_1_6_1,
            self.numpy_1_7_0])
        self.pool = Pool([repository])

    def test__add_decision(self):
        r_level = 1

        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions._add_decision(package.id, r_level)

        self.assertTrue(package.id in decisions._decision_map)
        self.assertEqual(decisions._decision_map[package.id], r_level)

        self.assertRaises(DepSolverError, lambda: decisions._add_decision(package.id, r_level+1))

    def test__add_decision_negated(self):
        r_level = 1

        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions._add_decision(-package.id, r_level)

        self.assertTrue(package.id in decisions._decision_map)
        self.assertEqual(decisions._decision_map[package.id], -r_level)

    def test_decide(self):
        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, 1, "because")

        self.assertTrue(package.id in decisions)
        self.assertEqual(len(decisions), 1)

    def test_is_decided(self):
        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, 1, "because")

        self.assertTrue(decisions.is_decided(package.id))
        self.assertFalse(decisions.is_decided(package.id + 1))

    def test_is_undecided(self):
        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, 1, "because")

        self.assertFalse(decisions.is_undecided(package.id))
        self.assertTrue(decisions.is_undecided(package.id + 1))

    def test_is_undecided(self):
        package1 = self.mkl_10_1_0
        package2 = self.mkl_10_2_0

        decisions = DecisionsSet(self.pool)
        decisions.decide(package1.id, 1, "because")
        decisions.decide(-package2.id, 1, "because")

        self.assertTrue(decisions.is_decided(package1.id))
        self.assertTrue(decisions.is_decided(package2.id))
        self.assertTrue(decisions.is_decided_install(package1.id))
        self.assertFalse(decisions.is_decided_install(package2.id))

    def test_satifsy(self):
        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, 1, "because")

        self.assertTrue(decisions.satisfy(package.id))
        self.assertFalse(decisions.satisfy(-package.id))
        self.assertFalse(decisions.satisfy(package.id + 1))

    def test_conflict(self):
        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, 1, "because")

        self.assertTrue(decisions.conflict(-package.id))
        self.assertFalse(decisions.conflict(package.id))

    def test_decision_level(self):
        r_level = 3

        package = self.mkl_10_1_0
        decisions = DecisionsSet(self.pool)
        decisions.decide(package.id, r_level, "because")

        self.assertEqual(decisions.decision_level(package.id), r_level)
        self.assertEqual(decisions.decision_level(-package.id), r_level)
        self.assertEqual(decisions.decision_level(package.id + 1), 0)

    def test_revert_last(self):
        r_level = 1

        decisions = DecisionsSet(self.pool)
        decisions.decide(self.mkl_10_1_0.id, r_level, "because")
        decisions.decide(self.numpy_1_7_0.id, r_level, "because because")

        self.assertEqual(len(decisions), 2)
        self.assertTrue(decisions.is_decided(self.mkl_10_1_0.id))
        self.assertTrue(decisions.is_decided(self.numpy_1_7_0.id))
        self.assertEqual(decisions.last_literal, self.numpy_1_7_0.id)
        self.assertEqual(decisions.last_reason, "because because")

        decisions.revert_last()

        self.assertEqual(len(decisions), 1)
        self.assertTrue(decisions.is_decided(self.mkl_10_1_0.id))
        self.assertTrue(decisions.is_undecided(self.numpy_1_7_0.id))
        self.assertTrue(decisions.last_literal, self.mkl_10_1_0.id)
        self.assertTrue(decisions.last_reason, "because because")

    def test_iter(self):
        """Check we iter from last to first."""
        r_ids = [self.mkl_10_2_0.id, self.mkl_10_1_0.id]

        decisions = DecisionsSet(self.pool)
        decisions.decide(self.mkl_10_1_0.id, 1, "because")
        decisions.decide(self.mkl_10_2_0.id, 2, "because because")

        self.assertEqual(list(decision.literal for decision in decisions), r_ids)
