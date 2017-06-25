import collections
import glob
import json
import subprocess
import tempfile

import os.path as op

import tempita
import yaml

from depsolver._package_utils \
    import \
        parse_package_full_name
from depsolver.package \
    import \
        parse_package_string, PackageInfo
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
from depsolver.solver.decisions \
    import \
        DecisionsSet
from depsolver.solver.rules_generator \
    import \
        RulesGenerator
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

P = PackageInfo.from_string
R = Requirement.from_string

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
        $this->jobs = $request->getJobs();

        $this->setupInstalledMap();

        $this->decisions = new Decisions($this->pool);

        $this->rules = $this->ruleSetGenerator->getRulesFor($this->jobs, $this->installedMap);
        $this->watchGraph = new RuleWatchGraph;

        foreach ($this->rules as $rule) {
            $this->watchGraph->insert(new RuleWatchNode($rule));
        }

        /* make decisions based on job/update assertions */
        $this->makeAssertionRuleDecisions();
        return $this->decisions;
    }
}

$policy = new DefaultPolicy();

$solver = new DebuggingSolver($policy, $pool, $installed_repo);
foreach($solver->print_decisions($request) as $operation) {
    $package_id = abs($operation[0]);
    $package = $pool->packageById($package_id);
    if ($decision[0] > 0) {
        printf("%s-%s;%s\n", $package->getName(), $package->getPrettyVersion(), $package_id);
    } else {
        printf("-%s-%s;%s\n", $package->getName(), $package->getPrettyVersion(), $package_id);
    }
}
"""

class MakeAssertionRulesScenario(HasTraits):
    solver = Instance(Solver)

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

    def compute_decisions(self):
        solver = Solver(self.pool, self.installed_repository)
        decisions, rules = solver._prepare_solver(self.request)
        solver._make_assertion_rules_decisions(decisions, rules)
        return decisions

    def to_php(self, filename="test_installed_map.php", composer_location=None):
        if composer_location is None:
            bootstrap_path = "__DIR__.'/src/bootstrap.php'"
        else:
            bootstrap_path = "'%s'" % op.join(composer_location, "src", "bootstrap.php")

        template = tempita.Template(TEMPLATE)

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

if __name__ == "__main__":
    data_directory = op.join(op.dirname(__file__), "data", "rules_generator")
    test_directory = op.join(op.dirname(__file__), "data", "make_assertion_rules")

    run_php_scenarios(data_directory, MakeAssertionRulesScenario, lambda x: x, test_directory)
