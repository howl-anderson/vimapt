import six

if not six.PY3:
    import unittest2 as unittest
else:
    import unittest

import os.path as op

from depsolver.pool \
    import \
        Pool
from depsolver.package \
    import \
        PackageInfo
from depsolver.repository \
    import \
        Repository
from depsolver.request \
    import \
        Request
from depsolver.requirement \
    import \
        Requirement
from depsolver.solver.core \
    import \
        Solver

from depsolver.solver.tests.scenarios.make_assertion_rules \
    import \
       MakeAssertionRulesScenario
from depsolver.solver.tests.scenarios.solver \
    import \
       SolverDecisionsScenario, SolverOperationsScenario

P = PackageInfo.from_string
R = Requirement.from_string

class TestInstallMapCase(unittest.TestCase):
    def _create_solver(self, installed_packages, remote_packages):
        installed_repo = Repository(installed_packages)
        remote_repo = Repository(remote_packages)
        pool = Pool([installed_repo, remote_repo])

        return Solver(pool, installed_repo)

    @unittest.expectedFailure
    def test_empty_installed_set(self):
        installed_packages = []
        remote_packages = [P("mkl-11.0.0")]

        solver = self._create_solver(installed_packages, remote_packages)

        request = Request(solver.pool)
        request.install(R("mkl"))

        solver._compute_package_maps(request)
        self.assertEqual(solver._id_to_installed_package, {})
        self.assertEqual(solver._id_to_updated_state, {})

    @unittest.expectedFailure
    def test_simple_install(self):
        installed_packages = [P("mkl-11.0.0")]
        remote_packages = [P("mkl-11.0.0")]

        solver = self._create_solver(installed_packages, remote_packages)

        request = Request(solver.pool)
        request.install(R("mkl"))

        solver._compute_package_maps(request)
        self.assertEqual(solver._id_to_installed_package, {1: P("mkl-11.0.0")})
        self.assertEqual(solver._id_to_updated_state, {})

    @unittest.expectedFailure
    def test_simple_update(self):
        installed_packages = [P("mkl-10.2.0")]
        remote_packages = [P("mkl-11.0.0")]

        solver = self._create_solver(installed_packages, remote_packages)

        request = Request(solver.pool)
        request.update(R("mkl"))

        solver._compute_package_maps(request)
        self.assertEqual(solver._id_to_installed_package, {1: P("mkl-10.2.0")})
        self.assertEqual(solver._id_to_updated_state, {1: True})

    @unittest.expectedFailure
    def test_simple_update_all(self):
        installed_packages = [P("mkl-10.2.0"), P("numpy-1.7.0")]
        remote_packages = [P("mkl-11.0.0"), P("numpy-1.7.1")]

        solver = self._create_solver(installed_packages, remote_packages)

        request = Request(solver.pool)
        request.upgrade()

        solver._compute_package_maps(request)
        self.assertEqual(solver._id_to_installed_package,
                         {1: P("mkl-10.2.0"), 2: P("numpy-1.7.0")})
        self.assertEqual(solver._id_to_updated_state, {1: True, 2: True})

class TestMakeAssertionRulesScenarios(unittest.TestCase):
    def _compute_decisions(self, scenario_description):
        data_directory = op.join(op.dirname(__file__), "scenarios", "data", "rules_generator")
        test_directory = op.join(op.dirname(__file__), "scenarios", "data", "make_assertion_rules")

        filename = op.join(data_directory, scenario_description)

        package_strings, package_ids = [], []
        fp = open(op.join(test_directory, op.splitext(scenario_description)[0] + ".test"))
        try:
            for line in fp:
                package, package_id = (part.strip() for part in line.split(";"))
                package_strings.append(package)
                package_ids.append(int(package_id))
        finally:
            fp.close()

        scenario = MakeAssertionRulesScenario.from_yaml(filename)
        decisions = scenario.compute_decisions()

        self.assertEqual(package_ids, list(decisions._decision_map.keys()))

    def test_complex_scenario1(self):
        scenario = "complex_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_complex_scenario2(self):
        scenario = "complex_scenario2.yaml"
        self._compute_decisions(scenario)

    def test_conflict_scenario1(self):
        scenario = "conflict_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_4_candidates(self):
        """Test rules creation for a single package wo dependencies and 4 candidates."""
        scenario = "multiple_provides_4_candidates.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_single_fulfilled_provides(self):
        """Test rules creation when multiple versions are available but only
        one fulfills the request."""
        scenario = "multiple_provides_single_fulfilled_provides.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_simple(self):
        """Test we generate obsolete rules when multiple candidates exist for a
        given package requirement."""
        scenario = "multiple_provides_simple.yaml"
        self._compute_decisions(scenario)

    def test_already_installed_indirect_provided(self):
        scenario = "multiple_provides_1_installed.yaml"
        self._compute_decisions(scenario)

    def test_replace_scenario1(self):
        scenario = "replace_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_replace_scenario2(self):
        scenario = "replace_scenario2.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_simple(self):
        scenario = "single_dependency_simple.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_installed_simple(self):
        scenario = "single_dependency_installed_simple.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_multiple_provides(self):
        scenario = "single_dependency_multiple_provides.yaml"
        self._compute_decisions(scenario)

class TestSolverDecisionsScenario(unittest.TestCase):
    def _compute_decisions(self, scenario_description):
        data_directory = op.join(op.dirname(__file__), "scenarios", "data", "rules_generator")
        test_directory = op.join(op.dirname(__file__), "scenarios", "data", "solver_decisions")

        filename = op.join(data_directory, scenario_description)

        r_package_strings, r_package_ids = [], []
        fp = open(op.join(test_directory, op.splitext(scenario_description)[0] + ".test"))
        try:
            for line in fp:
                package, package_id = (part.strip() for part in line.split(";"))
                r_package_strings.append(package)
                r_package_ids.append(int(package_id))
        finally:
            fp.close()

        scenario = SolverDecisionsScenario.from_yaml(filename)
        decisions = scenario.compute_decisions_set()
        package_ids = [abs(decision.literal) for decision in decisions]

        package_names = []
        for decision in decisions:
            package_id = abs(decision.literal)
            package_name = scenario.solver.pool.package_by_id(package_id).unique_name
            if decision.literal < 0:
                package_name = "-" + package_name
            package_names.append(package_name)

        self.assertEqual(r_package_ids, package_ids)

    def test_complex_scenario1(self):
        scenario = "complex_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_complex_scenario2(self):
        scenario = "complex_scenario2.yaml"
        self._compute_decisions(scenario)

    def test_conflict_scenario1(self):
        scenario = "conflict_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_4_candidates(self):
        """Test rules creation for a single package wo dependencies and 4 candidates."""
        scenario = "multiple_provides_4_candidates.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_single_fulfilled_provides(self):
        """Test rules creation when multiple versions are available but only
        one fulfills the request."""
        scenario = "multiple_provides_single_fulfilled_provides.yaml"
        self._compute_decisions(scenario)

    def test_multiple_provides_simple(self):
        """Test we generate obsolete rules when multiple candidates exist for a
        given package requirement."""
        scenario = "multiple_provides_simple.yaml"
        self._compute_decisions(scenario)

    def test_already_installed_indirect_provided(self):
        scenario = "multiple_provides_1_installed.yaml"
        self._compute_decisions(scenario)

    def test_replace_scenario1(self):
        scenario = "replace_scenario1.yaml"
        self._compute_decisions(scenario)

    def test_replace_scenario2(self):
        scenario = "replace_scenario2.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_simple(self):
        scenario = "single_dependency_simple.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_installed_simple(self):
        scenario = "single_dependency_installed_simple.yaml"
        self._compute_decisions(scenario)

    def test_single_dependency_multiple_provides(self):
        scenario = "single_dependency_multiple_provides.yaml"
        self._compute_decisions(scenario)

class TestSolverScenario(unittest.TestCase):
    def _compute_operations(self, scenario_description):
        data_directory = op.join(op.dirname(__file__), "scenarios", "data", "rules_generator")
        test_directory = op.join(op.dirname(__file__), "scenarios", "data", "solver_operations")

        filename = op.join(data_directory, scenario_description)

        fp = open(op.join(test_directory, op.splitext(scenario_description)[0] + ".test"))
        try:
            r_operation_strings = [line.rstrip() for line in fp]
        finally:
            fp.close()

        scenario = SolverOperationsScenario.from_yaml(filename)
        operations = scenario.compute_operations()

        self.assertEqual([str(operation) for operation in operations], r_operation_strings)

    def test_complex_scenario1(self):
        scenario = "complex_scenario1.yaml"
        self._compute_operations(scenario)

    def test_complex_scenario2(self):
        scenario = "complex_scenario2.yaml"
        self._compute_operations(scenario)

    def test_conflict_scenario1(self):
        scenario = "conflict_scenario1.yaml"
        self._compute_operations(scenario)

    def test_multiple_provides_4_candidates(self):
        """Test rules creation for a single package wo dependencies and 4 candidates."""
        scenario = "multiple_provides_4_candidates.yaml"
        self._compute_operations(scenario)

    def test_multiple_provides_numpy(self):
        """Test solver for a single package with dependencies and multiple
        candidates."""
        scenario = "multiple_provides_numpy.yaml"
        self._compute_operations(scenario)

    def test_multiple_provides_single_fulfilled_provides(self):
        """Test rules creation when multiple versions are available but only
        one fulfills the request."""
        scenario = "multiple_provides_single_fulfilled_provides.yaml"
        self._compute_operations(scenario)

    def test_multiple_provides_simple(self):
        """Test we generate obsolete rules when multiple candidates exist for a
        given package requirement."""
        scenario = "multiple_provides_simple.yaml"
        self._compute_operations(scenario)

    def test_already_installed_indirect_provided(self):
        scenario = "multiple_provides_1_installed.yaml"
        self._compute_operations(scenario)

    def test_replace_scenario1(self):
        scenario = "replace_scenario1.yaml"
        self._compute_operations(scenario)

    def test_replace_scenario2(self):
        scenario = "replace_scenario2.yaml"
        self._compute_operations(scenario)

    def test_single_dependency_simple(self):
        scenario = "single_dependency_simple.yaml"
        self._compute_operations(scenario)

    def test_single_dependency_installed_simple(self):
        scenario = "single_dependency_installed_simple.yaml"
        self._compute_operations(scenario)

    def test_single_dependency_multiple_provides(self):
        scenario = "single_dependency_multiple_provides.yaml"
        self._compute_operations(scenario)
