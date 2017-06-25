import os.path as op

import tempita

from depsolver.solver.core \
    import \
        Solver

from depsolver.bundled.traitlets \
    import \
        HasTraits, Dict, Instance, List, Long, Unicode

from depsolver.solver.tests.scenarios.common \
    import \
        COMMON_IMPORTS, COMPOSER_PATH, BaseScenario, packages_list_to_php_json, \
        requirement_to_php_string, requirement_string_to_php_constraints, \
        job_to_php_constraints, run_php_scenarios

DATA = op.join(op.dirname(__file__), "data", "rules_generator")

TEMPLATE = """\
<?php
require {{bootstrap_path}};

{{common_imports}}

$loader = new ArrayLoader();

/* Remote repository definition */
$remote_repo_json = '
{{remote_repo_json_string}}
';

$packages = JsonFile::parseJson($remote_repo_json);

$remote_repo = new WritableArrayRepository();
foreach ($packages as $packageData) {
    $package = $loader->load($packageData);
    $remote_repo->addPackage($package);
}

/* Installed repository definition */
$repo_json = '
{{installed_repo_json_string}}
';

$packages = JsonFile::parseJson($repo_json);

$installed_repo = new WritableArrayRepository();
foreach ($packages as $packageData) {
    $package = $loader->load($packageData);
    $installed_repo->addPackage($package);
}

/* Pool definition */
$pool = new Pool();
$pool->addRepository($remote_repo);
$pool->addRepository($installed_repo);

$request = new Request($pool);
{{for operation, requirement_name, constraints in request}}
$constraints = array(
    {{constraints}}
);
$request_constraints = new MultiConstraint($constraints);
$request->{{operation}}("{{requirement_name}}", $request_constraints);
{{endfor}}

class DebuggingSolver extends Solver
{
    public function print_decisions(Request $request)
    {
        $operations = $this->solve($request);
        foreach ($this->decisions as $decision) {
             $package_id = abs($decision[0]);
             $package = $this->pool->packageById($package_id);
             if ($decision[0] > 0) {
                 printf("%s-%s;%s\\n", $package->getName(), $package->getPrettyVersion(), $package_id);
             } else {
                 printf("-%s-%s;%s\\n", $package->getName(), $package->getPrettyVersion(), $package_id);
             }
        }
    }

    public function print_operations(Request $request)
    {
        $operations = $this->solve($request);
        foreach ($operations as $operation) {
             print("$operation\\n");
        }
    }
}

$policy = new DefaultPolicy();
"""

DECISIONS_TEMPLATE = TEMPLATE + """
$solver = new DebuggingSolver($policy, $pool, $installed_repo);
$solver->print_decisions($request);
"""

OPERATIONS_TEMPLATE = TEMPLATE + """
$solver = new DebuggingSolver($policy, $pool, $installed_repo);
$solver->print_operations($request);
"""

class SolverDecisionsScenario(HasTraits):
    solver = Instance(Solver)
    template_string = Unicode(DECISIONS_TEMPLATE)

    _base_scenario = Instance(BaseScenario)

    @property
    def remote_repository(self):
        return self._base_scenario.remote_repository

    @property
    def installed_repository(self):
        return self._base_scenario.installed_repository

    @property
    def pool(self):
        return self._base_scenario.pool

    @property
    def request(self):
        return self._base_scenario.request

    @classmethod
    def from_yaml(cls, filename):
        base_scenario = BaseScenario.from_yaml(filename)
        solver = Solver(base_scenario.pool, base_scenario.installed_repository)
        return cls(_base_scenario=base_scenario, solver=solver)

    def compute_decisions_set(self):
        """
        Compute the decisions set for this scenario.
        """
        return self.solver._solve(self.request)

    def to_php(self, filename, composer_location=None):
        if composer_location is None:
            bootstrap_path = "__DIR__.'/src/bootstrap.php'"
        else:
            bootstrap_path = "'%s'" % op.join(composer_location, "src", "bootstrap.php")

        template = tempita.Template(self.template_string)

        remote_packages = self.remote_repository.list_packages()
        installed_packages = self.installed_repository.list_packages()

        variables = {
                "bootstrap_path": bootstrap_path,
                "remote_repo_json_string": packages_list_to_php_json(remote_packages),
                "installed_repo_json_string": packages_list_to_php_json(installed_packages),
                "request": [(job.job_type, job.requirement.name, job_to_php_constraints(job)) \
                            for job in self.request.jobs],
                "common_imports": COMMON_IMPORTS,
        }
        with open(filename, "wt") as fp:
            fp.write(template.substitute(variables))

class SolverOperationsScenario(SolverDecisionsScenario):
    template_string = Unicode(OPERATIONS_TEMPLATE)

    def compute_operations(self):
        """
        Compute the operations for this scenario.
        """
        return self.solver.solve(self.request)

if __name__ == "__main__":
    data_directory = op.join(op.dirname(__file__), "data", "rules_generator")
    decisions_test_directory = op.join(op.dirname(__file__), "data", "solver_decisions")
    operations_test_directory = op.join(op.dirname(__file__), "data", "solver_operations")

    run_php_scenarios(data_directory, SolverDecisionsScenario, lambda x: x, decisions_test_directory)
    run_php_scenarios(data_directory, SolverOperationsScenario, lambda x: x, operations_test_directory)
