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
from depsolver.request \
    import \
        _Job, Request
from depsolver.requirement \
    import \
        Requirement
from depsolver.version \
    import \
        SemanticVersion

P = PackageInfo.from_string
V = SemanticVersion.from_string
R = Requirement.from_string

class TestRequest(unittest.TestCase):
    def setUp(self):
        self.mkl_10_3_0 = P("mkl-10.3.0")
        self.mkl_11_0_0 = P("mkl-11.0.0")

        self.numpy_1_7_0 = P("numpy-1.7.0; depends (mkl >= 11.0.0)")

        self.scipy_0_12_0 = P("scipy-0.12.0; depends (numpy >= 1.7.0)")

        repo = Repository([self.mkl_10_3_0, self.mkl_11_0_0, self.numpy_1_7_0, self.scipy_0_12_0])
        self.pool = Pool([repo])

    def test_simple_install(self):
        r_jobs = [
            _Job([self.scipy_0_12_0], "install", R("scipy")),
            _Job([self.numpy_1_7_0], "install", R("numpy")),
        ]

        request = Request(self.pool)
        request.install(R("scipy"))
        request.install(R("numpy"))

        self.assertEqual(request.jobs, r_jobs)

    def test_simple_update(self):
        r_jobs = [
            _Job([self.numpy_1_7_0], "update", R("numpy")),
        ]

        request = Request(self.pool)
        request.update(R("numpy"))

        self.assertEqual(request.jobs, r_jobs)

    def test_simple_remove(self):
        r_jobs = [
            _Job([self.numpy_1_7_0], "remove", R("numpy")),
        ]

        request = Request(self.pool)
        request.remove(R("numpy"))

        self.assertEqual(request.jobs, r_jobs)

    def test_simple_upgrade(self):
        r_jobs = [_Job([], "upgrade", None)]

        request = Request(self.pool)
        request.upgrade()

        self.assertEqual(request.jobs, r_jobs)
