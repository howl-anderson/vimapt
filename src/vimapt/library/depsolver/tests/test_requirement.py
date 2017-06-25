import unittest

from depsolver.errors \
    import \
        DepSolverError
from depsolver.requirement \
    import \
        Requirement, RequirementParser
from depsolver.requirement_parser \
    import \
        Any, Equal, GEQ, LEQ
from depsolver.version \
    import \
        SemanticVersion

V = SemanticVersion.from_string

class TestRequirementParser(unittest.TestCase):
    def test_simple(self):
        parser = RequirementParser()

        r_requirements = [Requirement("numpy", [GEQ("1.3.0")])]
        requirements = parser.parse("numpy >= 1.3.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [GEQ("1.3.0"),
                                                LEQ("2.0.0")])]
        requirements = parser.parse("numpy >= 1.3.0, numpy <= 2.0.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [Equal("1.3.0")])]
        requirements = parser.parse("numpy == 1.3.0")
        self.assertEqual(r_requirements, list(requirements))

        r_requirements = [Requirement("numpy", [Equal("1.3.0"),
                                                Equal("1.4.0")])]
        requirements = parser.parse("numpy == 1.3.0, numpy == 1.4.0")
        self.assertEqual(r_requirements, list(requirements))
        self.assertTrue(requirements[0]._cannot_match)

        r_requirements = [Requirement("numpy", [Any()])]
        requirements = parser.parse("numpy")
        self.assertEqual(r_requirements, list(requirements))

    def test_repr(self):
        parser = RequirementParser()

        requirement_string = "numpy >= 1.3.0, numpy <= 2.0.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), requirement_string)

        requirement_string = "numpy"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy *")

        requirement_string = "numpy == 1.2.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy == 1.2.0")

        requirement_string = "numpy == 1.3.0, numpy == 1.4.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy None")

        requirement_string = "numpy > 1.3.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy > 1.3.0")

        requirement_string = "numpy < 1.3.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy < 1.3.0")

        requirement_string = "numpy != 1.3.0"
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(repr(numpy_requirement), "numpy != 1.3.0")

    def test_from_string(self):
        requirement_string = "numpy >= 1.3.0, numpy <= 2.0.0"
        parser = RequirementParser()
        numpy_requirement = list(parser.parse(requirement_string))[0]

        self.assertEqual(numpy_requirement, Requirement.from_string(requirement_string))

        self.assertRaises(DepSolverError,
                lambda: Requirement.from_string("numpy <= 1.2.0, scipy >= 2.3.2"))

    def test_matches_simple(self):
        R = Requirement.from_string

        numpy_requirement = R("numpy >= 1.3.0, numpy <= 1.4.0")
        # provide is an equality constraint
        self.assertTrue(numpy_requirement.matches(R("numpy")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.2.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy == 1.3.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy == 1.4.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.5.0")))

        # provide is a different name
        self.assertFalse(numpy_requirement.matches(R("numpypy == 1.3.0")))

        # provide is a range
        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.3.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.4.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy >= 1.5.0")))

        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.3.0, numpy <= 1.5.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.4.0, numpy <= 1.5.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy >= 1.5.0, numpy <= 1.5.0")))

        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.2.0, numpy <= 1.3.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy >= 1.2.0, numpy <= 1.2.5")))

        numpy_requirement = R("numpy == 1.3.0")
        self.assertTrue(numpy_requirement.matches(R("numpy == 1.3.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.2.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.3.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy <= 1.4.0")))

    def test_match_strict(self):
        R = Requirement.from_string

        numpy_requirement = R("numpy > 1.3.0, numpy < 1.4.0")
        self.assertTrue(numpy_requirement.matches(R("numpy == 1.3.5")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.3.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.4.0")))
        self.assertTrue(numpy_requirement.matches(R("numpy >= 1.3.2, numpy <= 1.3.4")))
        self.assertTrue(numpy_requirement.matches(R("numpy != 1.3.2")))

    def test_composite(self):
        R = Requirement.from_string

        numpy_requirement = R("numpy >= 1.3.0, numpy <= 1.5.0, numpy <= 1.4.0")
        r_numpy_requirement = R("numpy >= 1.3.0, numpy <= 1.4.0")
        self.assertEqual(numpy_requirement, r_numpy_requirement)

    def test_matches_nomatch(self):
        R = Requirement.from_string

        numpy_requirement = R("numpy >= 1.3.0, numpy <= 1.2.0")
        self.assertFalse(numpy_requirement.matches(R("numpy")))

    def test_matches_strict(self):
        R = Requirement.from_string

        numpy_requirement = R("numpy > 1.3.0, numpy < 1.4.0")
        self.assertTrue(numpy_requirement.matches(R("numpy")))
        self.assertTrue(numpy_requirement.matches(R("numpy == 1.3.5")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.3.0")))
        self.assertFalse(numpy_requirement.matches(R("numpy == 1.4.0")))

    def test_from_package_string(self):
        R = Requirement.from_string

        r_requirement = R("numpy == 1.3.0")

        requirement = Requirement.from_package_string("numpy-1.3.0")

        self.assertEqual(requirement, r_requirement)
