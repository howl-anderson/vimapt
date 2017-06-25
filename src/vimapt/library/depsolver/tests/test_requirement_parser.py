import unittest

from depsolver.constraints \
    import \
        Any, Equal, GEQ, GT, LEQ, LT, Not
from depsolver.errors \
    import \
        DepSolverError
from depsolver.requirement_parser \
    import \
        RawRequirementParser, CommaToken, DistributionNameToken, EqualToken, \
        GEQToken, GTToken, LEQToken, LTToken, NotToken, VersionToken

class TestRawRequirementParser(unittest.TestCase):
    def test_lexer_simple(self):
        r_tokens = [DistributionNameToken("numpy"), GEQToken(">="),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy >= 1.3.0"))
        self.assertEqual(tokens, r_tokens)

        r_tokens = [DistributionNameToken("numpy"), LEQToken("<="),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy <= 1.3.0"))
        self.assertEqual(tokens, r_tokens)

        r_tokens = [DistributionNameToken("numpy"), EqualToken("=="),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy == 1.3.0"))
        self.assertEqual(tokens, r_tokens)

        r_tokens = [DistributionNameToken("numpy"), GTToken(">"),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy > 1.3.0"))
        self.assertEqual(tokens, r_tokens)

        r_tokens = [DistributionNameToken("numpy"), LTToken("<"),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy < 1.3.0"))
        self.assertEqual(tokens, r_tokens)

    def test_not_token(self):
        r_tokens = [DistributionNameToken("numpy"), NotToken("!="),
                VersionToken("1.3.0")]
        tokens = list(RawRequirementParser().tokenize("numpy != 1.3.0"))
        self.assertEqual(tokens, r_tokens)

    def test_lexer_invalids(self):
        parser = RawRequirementParser()
        self.assertRaises(DepSolverError,
                lambda : parser.parse("numpy >= 1.2.3 | numpy <= 2.0.0"))

    def test_lexer_compounds(self):
        r_tokens = [DistributionNameToken("numpy"), GEQToken(">="),
                VersionToken("1.3.0"), CommaToken(","),
                DistributionNameToken("numpy"), LEQToken("<="),
                VersionToken("2.0.0")]
        tokens = list(RawRequirementParser().tokenize("numpy >= 1.3.0, numpy <= 2.0.0"))
        self.assertEqual(tokens, r_tokens)

    def test_parser_simple(self):
        parse_dict = RawRequirementParser().parse("numpy >= 1.3.0")
        self.assertEqual(dict(parse_dict), {"numpy": [GEQ("1.3.0")]})

        parse_dict = RawRequirementParser().parse("numpy <= 1.3.0")
        self.assertEqual(dict(parse_dict), {"numpy": [LEQ("1.3.0")]})

        parse_dict = RawRequirementParser().parse("numpy == 1.3.0")
        self.assertEqual(dict(parse_dict), {"numpy": [Equal("1.3.0")]})

        parse_dict = RawRequirementParser().parse("numpy != 1.3.0")
        self.assertEqual(dict(parse_dict), {"numpy": [Not("1.3.0")]})

    def test_parser_invalids(self):
        parser = RawRequirementParser()
        self.assertRaises(DepSolverError, lambda : parser.parse("numpy >= "))

    def test_parser_glob(self):
        parser = RawRequirementParser()

        r_constraints = {"numpy": [GEQ("1.0.0"), LT("2.0.0")]}
        self.assertEqual(parser.parse("numpy == 1.*"), r_constraints)

        r_constraints = {"numpy": [GEQ("1.3.0"), LT("1.4.0")]}
        parser = RawRequirementParser()

        self.assertEqual(parser.parse("numpy == 1.3.*"), r_constraints)

        self.assertRaises(NotImplementedError, lambda : parser.parse("numpy == 1.*-build"))
        self.assertRaises(NotImplementedError, lambda : parser.parse("numpy == 1.0.0-b*"))

    def test_parser_compounds(self):
        parse_dict = RawRequirementParser().parse("numpy >= 1.3.0, numpy <= 2.0.0")
        self.assertEqual(dict(parse_dict), {
                    "numpy": [
                        GEQ("1.3.0"), LEQ("2.0.0"),
                    ]
                })

        parse_dict = RawRequirementParser().parse("numpy > 1.3.0, numpy < 2.0.0")
        self.assertEqual(dict(parse_dict), {
                    "numpy": [
                        GT("1.3.0"), LT("2.0.0"),
                    ]
                })

    def test_any_simple(self):
        r_constraints = {"numpy": [Any()]}
        parser = RawRequirementParser()

        self.assertEqual(parser.parse("numpy *"), r_constraints)
