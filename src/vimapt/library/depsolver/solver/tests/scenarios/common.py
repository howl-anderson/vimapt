import collections
import glob
import json
import subprocess
import tempfile

import os.path as op

import yaml

from depsolver.bundled.traitlets \
    import \
        HasTraits, Dict, Instance, List, Long, Unicode
from depsolver.constraints \
    import \
        Any, GEQ, LT
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
from depsolver.requirement_parser \
    import \
        RawRequirementParser

COMMON_IMPORTS = """\
use Composer\DependencyResolver\Decisions;
use Composer\DependencyResolver\DefaultPolicy;
use Composer\DependencyResolver\Pool;
use Composer\DependencyResolver\Request;
use Composer\DependencyResolver\RuleWatchGraph;
use Composer\DependencyResolver\RuleWatchNode;
use Composer\DependencyResolver\Solver;
use Composer\DependencyResolver\Transaction;
use Composer\Json\JsonFile;
use Composer\Package\CompletePackage;
use Composer\Package\Link;
use Composer\Package\LinkConstraint\MultiConstraint;
use Composer\Package\LinkConstraint\VersionConstraint;
use Composer\Package\Loader\ArrayLoader;
use Composer\Repository\ArrayRepository;
use Composer\Repository\FilesystemRepository;
use Composer\Repository\InstalledFilesystemRepository;
use Composer\Repository\WritableArrayRepository;

"""

COMPOSER_PATH = "/Users/cournape/src/dev/composer/composer-git"
#COMPOSER_PATH = "/home/davidc/src/projects/composer-git"

P = PackageInfo.from_string
R = Requirement.from_string

def requirement_to_php_string(req):
    s = str(req)
    parts = (part.split() for part in s.split(","))

    ret = []
    for part in parts:
        ret.append(" ".join(part[1:]))
    return ", ".join(ret)

def requirements_to_php_dict(requirements):
    php_dict = collections.defaultdict(list)
    for requirement in requirements:
        php_dict[requirement.name].append(requirement_to_php_string(requirement))

    return dict((k, ", ".join(v)) for k, v in php_dict.items())

def packages_list_to_php_json(packages):
    res = []
    for package in packages:
        version_normalized = str(package.version) + ".0"
        res.append({
                "name": package.name,
                "version": str(package.version),
                "version_normalized": version_normalized,
                "provide": requirements_to_php_dict(package.provides),
                "require": requirements_to_php_dict(package.dependencies),
                "conflict": requirements_to_php_dict(package.conflicts),
                "replace": requirements_to_php_dict(package.replaces),
        })
    return json.dumps(res, indent=4)

def requirement_string_to_php_constraints(req):
    ret = []

    parser = RawRequirementParser()
    reqs = parser.parse(req).items()
    if not len(reqs) == 1:
        raise ValueError()

    for name, constraints in reqs:
        for constraint in constraints:
            if isinstance(constraint, GEQ):
                ret.append((">=", constraint.version))
            elif isinstance(constraint, LT):
                ret.append(("<", constraint.version))
            elif isinstance(constraint, Any):
                pass
            else:
                raise ValueError("Unsupported constraint: %s" % constraint)

    return ret

def job_to_php_constraints(job):
    """
    Extract requirements from a _Job instance into a comma-separated string of
    php requirements.
    """
    s = str(job.requirement)

    constraints = ['new VersionConstraint("%s", "%s")' % \
                   (ret[0], ret[1]) \
                    for ret in requirement_string_to_php_constraints(s)]
    return ',\n'.join(constraints)

class BaseScenario(HasTraits):
    remote_repository = Instance(Repository)
    installed_repository = Instance(Repository)

    pool = Instance(Pool)
    request = Instance(Request)

    @classmethod
    def from_yaml(cls, filename):
        with open(filename, "rt") as fp:
            raw_data = yaml.load(fp)

        packages = [P(s) for s in raw_data.get("packages", [])]
        package_name_to_package = {}
        for package in packages:
            package_name_to_package[package.unique_name] = package

        raw_installed_packages = raw_data.get("installed_repository", []) or []
        installed_packages = [package_name_to_package[package_name] \
                                for package_name in raw_installed_packages]
            
        raw_remote_packages = raw_data.get("remote_repository", []) or []
        remote_packages = [package_name_to_package[package_name] \
                             for package_name in raw_remote_packages]

        request_data = [(r["operation"], r["requirement"]) \
                        for r in raw_data.get("request", []) or []]

        return cls.from_data(remote_packages=remote_packages,
                installed_packages=installed_packages,
                request_jobs=request_data)

    @classmethod
    def from_data(cls, remote_packages, installed_packages, request_jobs):
        remote_repository = Repository(packages=[P(p.package_string) for p in remote_packages])
        installed_repository = Repository(packages=[P(p.package_string) for p in installed_packages])

        pool = Pool([remote_repository, installed_repository])
        request = Request(pool)
        for name, requirement_string in request_jobs:
            getattr(request, name)(R(requirement_string))

        return cls(remote_repository=remote_repository,
                   installed_repository=installed_repository,
                   pool=pool, request=request)

def run_php_scenarios(data_directory, scenario_class, post_process, test_directory=None):
    if test_directory is None:
        test_directory = data_directory

    for path in glob.glob(op.join(data_directory, "*.yaml")):
        php_file = op.splitext(path)[0] + ".php"
        print(path)
        print(php_file)
        test_file = op.splitext(op.join(test_directory, op.basename(path)))[0] + ".test"

        scenario = scenario_class.from_yaml(path)
        scenario.to_php(php_file, composer_location=COMPOSER_PATH)
        with tempfile.NamedTemporaryFile(suffix=".php") as fp:
            scenario.to_php(fp.name, composer_location=COMPOSER_PATH)

            with open(test_file, "wt") as ofp:
                output = subprocess.check_output(["php", fp.name])
                ofp.write(post_process(output))
