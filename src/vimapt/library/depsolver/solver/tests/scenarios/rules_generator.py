import os.path as op

import tempita

from depsolver._package_utils \
    import \
        parse_package_full_name
from depsolver.compat \
    import \
        OrderedDict
from depsolver.package \
    import \
        PackageInfo
from depsolver.requirement \
    import \
        Requirement
from depsolver.solver.rules_generator \
    import \
        RulesGenerator

from depsolver.bundled.traitlets \
    import \
        HasTraits, Instance

from depsolver.solver.tests.scenarios.common \
    import \
        COMMON_IMPORTS, BaseScenario, packages_list_to_php_json, \
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
    public function printRules(Request $request)
    {
        $this->jobs = $request->getJobs();

        $this->setupInstalledMap();

        $this->decisions = new Decisions($this->pool);

        $this->rules = $this->ruleSetGenerator->getRulesFor($this->jobs, $this->installedMap);
        $this->watchGraph = new RuleWatchGraph;

        foreach ($this->rules as $rule) {
            printf("%s\\n", $rule);
        }
    }
}

$policy = new DefaultPolicy();

$solver = new DebuggingSolver($policy, $pool, $installed_repo);
$solver->printRules($request);
"""

class RulesGeneratorScenario(HasTraits):
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
        return cls(_base_scenario=base_scenario)

    @classmethod
    def from_data(cls, remote_packages, installed_packages, request_jobs):
        base_scenario = BaseScenario.from_data(filename)
        return cls(_base_scenario=base_scenario)

    def compute_rules(self):
        installed_map = OrderedDict()
        for package in self.installed_repository.iter_packages():
            installed_map[package.id] = package
        rules_generator = RulesGenerator(self.pool, self.request, installed_map)
        return list(rules_generator.iter_rules())

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

def post_process(output):
    """Crappy function to convert php rule string to depsolver ones."""
    lines = []
    for line in output.splitlines():
        new_parts = []
        parts = [p.strip() for p in line[1:-1].split("|")]
        for part in parts:
            if part.startswith("-"):
                part = part[1:-2]
                name, version = parse_package_full_name(part)
                new_part = "-" + "%s-%s" % (name, str(version))
            else:
                part = part[:-2]
                name, version = parse_package_full_name(part)
                new_part = "%s-%s" % (name, str(version))
            new_parts.append(new_part)
        lines.append("(" + " | ".join(new_parts) + ")")
    lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    data_directory = op.join(op.dirname(__file__), "data", "rules_generator")
    run_php_scenarios(data_directory, RulesGeneratorScenario, post_process)
