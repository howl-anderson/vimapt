import six

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

import os.path as op

from depsolver.compat \
    import \
        OrderedDict
from depsolver.package \
    import \
        PackageInfo
from depsolver.pool \
    import \
        Pool
from depsolver.repository \
    import \
        Repository
from depsolver.request \
    import \
        Request
from depsolver.requirement \
    import \
        Requirement

from depsolver.solver.rules_generator \
    import \
        RulesSet, RulesGenerator
from depsolver.solver.rule \
    import \
        PackageRule

from depsolver.solver.tests.scenarios.rules_generator \
    import \
       DATA, RulesGeneratorScenario

P = PackageInfo.from_string
R = Requirement.from_string

class TestPackageRule(unittest.TestCase):
    def setUp(self):
        self.mkl_10_1_0 = P("mkl-10.1.0")
        self.mkl_10_2_0 = P("mkl-10.2.0")
        self.mkl_10_3_0 = P("mkl-10.3.0")
        self.mkl_11_0_0 = P("mkl-11.0.0")

        self.numpy_1_6_0 = P("numpy-1.6.0; depends (mkl)")
        self.numpy_1_6_1 = P("numpy-1.6.1; depends (mkl)")
        self.numpy_1_7_0 = P("numpy-1.7.0; depends (mkl)")

        self.nomkl_numpy_1_6_0 = P("nomkl_numpy-1.6.0; provides(numpy == 1.6.0)")
        self.nomkl_numpy_1_6_1 = P("nomkl_numpy-1.6.1; provides(numpy == 1.6.1)")
        self.nomkl_numpy_1_7_0 = P("nomkl_numpy-1.7.0; provides(numpy == 1.7.0)")

        self.mkl_numpy_1_6_1 = P("mkl_numpy-1.6.1; provides(numpy == 1.6.1); depends (mkl)")
        self.mkl_numpy_1_7_0 = P("mkl_numpy-1.7.0; provides(numpy == 1.7.0); depends (mkl)")

        self.scipy_0_11_0 = P("scipy-0.11.0; depends (numpy >= 1.4.0)")
        self.scipy_0_12_0 = P("scipy-0.12.0; depends (numpy >= 1.4.0)")

        self.matplotlib_1_2_0 = P("matplotlib-1.2.0; depends (numpy >= 1.6.0)")

        repo = Repository([self.mkl_10_1_0, self.mkl_10_2_0, self.mkl_10_3_0,
                           self.mkl_11_0_0, self.numpy_1_6_0])
        pool = Pool()
        pool.add_repository(repo)

        self.pool = pool

    def test_str(self):
        rule = PackageRule.from_packages(self.pool, [self.mkl_11_0_0,
                                         self.mkl_10_1_0, self.mkl_10_2_0], None)
        rule_repr = str(rule)
        self.assertEqual(rule_repr, "(+mkl-10.1.0 | +mkl-10.2.0 | +mkl-11.0.0)")

        rule_repr = str(PackageRule(self.pool, [-self.mkl_10_2_0.id, self.mkl_11_0_0.id], None))
        self.assertEqual(rule_repr, "(-mkl-10.2.0 | +mkl-11.0.0)")

    def test_from_package_string(self):
        r_rule = PackageRule.from_packages(self.pool, [self.mkl_11_0_0], None)

        rule = PackageRule.from_string(self.pool, "mkl-11.0.0", None)
        self.assertTrue(rule.is_equivalent(r_rule))

        r_rule = PackageRule.from_packages(self.pool, [self.mkl_10_2_0, self.mkl_11_0_0], None)
        rule = PackageRule.from_string(self.pool, "mkl-10.2.0 | mkl-11.0.0", None)
        self.assertTrue(rule.is_equivalent(r_rule))

        r_rule = PackageRule(self.pool, [-self.mkl_10_2_0.id, self.mkl_11_0_0.id], None)
        rule = PackageRule.from_string(self.pool, "-mkl-10.2.0 | mkl-11.0.0", None)
        self.assertTrue(rule.is_equivalent(r_rule))

        r_rule = PackageRule(self.pool, [-self.mkl_10_2_0.id, -self.mkl_11_0_0.id], None)
        rule = PackageRule.from_string(self.pool, "-mkl-10.2.0 | -mkl-11.0.0", None)
        self.assertTrue(rule.is_equivalent(r_rule))

class TestCreateClauses(unittest.TestCase):
    def setUp(self):
        self.mkl_10_1_0 = P("mkl-10.1.0")
        self.mkl_10_2_0 = P("mkl-10.2.0")
        self.mkl_10_3_0 = P("mkl-10.3.0")
        self.mkl_11_0_0 = P("mkl-11.0.0")

        self.numpy_1_6_0 = P("numpy-1.6.0; depends (mkl)")

        repo = Repository([self.mkl_10_1_0, self.mkl_10_2_0, self.mkl_10_3_0,
            self.mkl_11_0_0, self.numpy_1_6_0])
        pool = Pool()
        pool.add_repository(repo)

        self.pool = pool

    def test_create_depends_rule(self):
        r_rule = PackageRule.from_string(self.pool,
                    "-numpy-1.6.0 | mkl-10.1.0 | mkl-10.2.0 | mkl-10.3.0 | mkl-11.0.0",
                    None)

        req = R("numpy")
        request = Request(self.pool)
        request.install(req)

        rules_generator = RulesGenerator(self.pool, request, OrderedDict())
        dependencies = self.pool.what_provides(self.numpy_1_6_0.dependencies[0])
        rule = rules_generator._create_dependency_rule(self.numpy_1_6_0, dependencies, None)

        self.assertTrue(rule.is_equivalent(r_rule))

    @unittest.expectedFailure
    def test_iter_conflict_rules(self):
        # Making sure single package corner-case works
        self.assertEqual(set(), set(iter_conflict_rules(self.pool, [mkl_10_1_0])))

        # 3 packages conflicting with each other -> 3 rules (C_3^2)
        r_rules = set()
        r_rules.add(PackageRule.from_string("-mkl-10.1.0 | -mkl-10.2.0", self.pool))
        r_rules.add(PackageRule.from_string("-mkl-10.1.0 | -mkl-10.3.0", self.pool))
        r_rules.add(PackageRule.from_string("-mkl-10.2.0 | -mkl-10.3.0", self.pool))

        self.assertEqual(r_rules,
                set(iter_conflict_rules(self.pool, [mkl_10_1_0, mkl_10_2_0, mkl_10_3_0])))

class TestRulesSet(unittest.TestCase):
    def test_simple(self):
        repository = Repository([P("mkl-10.1.0"),
                                 P("numpy-1.7.0; depends (MKL >= 10.1.0)"),
                                 P("scipy-0.12.0; depends (numpy >= 1.7.0)")])
        pool = Pool([repository])

        rule = PackageRule(pool, [1, 2], "job_install", "scipy")

        rules_set = RulesSet()
        rules_set.add_rule(rule, "package")

        self.assertEqual(len(rules_set), 1)

class TestRulesGeneratorScenarios(unittest.TestCase):
    def _compute_rules(self, scenario_description):
        filename = op.join(DATA, scenario_description)
        
        fp = open(op.join(DATA, op.splitext(scenario_description)[0] + ".test"))
        try:
            r_rules = [line.rstrip() for line in fp]
        finally:
            fp.close()

        scenario = RulesGeneratorScenario.from_yaml(filename)
        rules = [str(r) for r in scenario.compute_rules()]

        self.assertEqual(r_rules, rules)

    def test_buggy_scenario(self):
        scenario = "buggy_scenario.yaml"
        self._compute_rules(scenario)

    def test_complex_scenario1(self):
        scenario = "complex_scenario1.yaml"
        self._compute_rules(scenario)

    def test_complex_scenario2(self):
        scenario = "complex_scenario2.yaml"
        self._compute_rules(scenario)

    def test_conflict_scenario1(self):
        scenario = "conflict_scenario1.yaml"
        self._compute_rules(scenario)

    def test_multiple_provides_4_candidates(self):
        """Test rules creation for a single package wo dependencies and 4 candidates."""
        scenario = "multiple_provides_4_candidates.yaml"
        self._compute_rules(scenario)

    def test_multiple_provides_numpy(self):
        """Test rules creation for a single package with dependencies and
        multiple candidates."""
        scenario = "multiple_provides_numpy.yaml"
        self._compute_rules(scenario)

    def test_multiple_provides_single_fulfilled_provides(self):
        """Test rules creation when multiple versions are available but only
        one fulfills the request."""
        scenario = "multiple_provides_single_fulfilled_provides.yaml"
        self._compute_rules(scenario)

    def test_multiple_provides_simple(self):
        """Test we generate obsolete rules when multiple candidates exist for a
        given package requirement."""
        scenario = "multiple_provides_simple.yaml"
        self._compute_rules(scenario)

    def test_already_installed_indirect_provided(self):
        scenario = "multiple_provides_1_installed.yaml"
        self._compute_rules(scenario)

    def test_replace_scenario1(self):
        scenario = "replace_scenario1.yaml"
        self._compute_rules(scenario)

    def test_replace_scenario2(self):
        scenario = "replace_scenario2.yaml"
        self._compute_rules(scenario)

    def test_single_dependency_simple(self):
        scenario = "single_dependency_simple.yaml"
        self._compute_rules(scenario)

    def test_single_dependency_installed_simple(self):
        scenario = "single_dependency_installed_simple.yaml"
        self._compute_rules(scenario)

    def test_single_dependency_multiple_provides(self):
        scenario = "single_dependency_multiple_provides.yaml"
        self._compute_rules(scenario)
