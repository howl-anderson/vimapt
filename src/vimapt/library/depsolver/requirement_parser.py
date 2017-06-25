import re

import six

from .compat \
    import \
        OrderedDict
from .errors \
    import \
        DepSolverError, InvalidVersion
from .constraints \
    import \
        Any, Equal, GEQ, GT, LEQ, LT, Not
from .version \
    import \
        _LOOSE_VERSION_RE

_DEFAULT_SCANNER = re.Scanner([
    (r"[a-zA-Z_]\w*", lambda scanner, token: DistributionNameToken(token)),
    (r"[^=><!,\s][^,\s]+", lambda scanner, token: VersionToken(token)),
    (r"==", lambda scanner, token: EqualToken(token)),
    (r">=", lambda scanner, token: GEQToken(token)),
    (r">", lambda scanner, token: GTToken(token)),
    (r"<=", lambda scanner, token: LEQToken(token)),
    (r"<", lambda scanner, token: LTToken(token)),
    (r"!=", lambda scanner, token: NotToken(token)),
    (",", lambda scanner, token: CommaToken(token)),
    (r"\*", lambda scanner, token: AnyToken(token)),
    (" +", lambda scanner, token: None),
])

class Token(object):
    typ = None
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

    # Mostly useful for testing
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

class CommaToken(Token):
    typ = "comma"

class DistributionNameToken(Token):
    typ = "distribution_name"

class AnyToken(Token):
    typ = "any"

class VersionToken(Token):
    typ = "version"

class ComparisonToken(Token):
    typ = "comparison"

class LEQToken(ComparisonToken):
    typ = "leq"

class LTToken(ComparisonToken):
    typ = "lt"

class GEQToken(ComparisonToken):
    typ = "geq"

class GTToken(ComparisonToken):
    typ = "gt"

class EqualToken(ComparisonToken):
    typ = "equal"

class NotToken(ComparisonToken):
    typ = "not"

def iter_over_requirement(tokens):
    """Yield a single requirement 'block' (i.e. a sequence of tokens between
    comma).

    Parameters
    ----------
    tokens: iterator
        Iterator of tokens
    """
    while True:
        block = []
        token = six.advance_iterator(tokens)
        try:
            while not isinstance(token, CommaToken):
                block.append(token)
                token = six.advance_iterator(tokens)
            yield block
        except StopIteration as e:
            yield block
            raise e

_OPERATOR_TO_SPEC = {
        EqualToken: Equal,
        GEQToken: GEQ,
        GTToken: GT,
        LEQToken: LEQ,
        LTToken: LT,
        NotToken: Not,
}

def _spec_factory(comparison_token):
    klass = _OPERATOR_TO_SPEC.get(comparison_token.__class__, None)
    if klass is None:
        raise DepSolverError("Unsupported comparison token %s" % comparison_token)
    else:
        return klass

def _is_glob_version(version_string):
    return "*" in version_string

def _glob_version_to_constraints(version_string):
    # This won't win a beauty prize
    n_stars = version_string.count("*")
    if n_stars == 0 or n_stars > 1:
        raise InvalidVersion("version string %r is not a valid glob version" % version_string)
    else:
        if "-" in version_string or "+" in version_string:
            raise NotImplementedError("glob version witg dev/release parts not supported yet")

        left_part = version_string[:version_string.index("*")]

        if not _LOOSE_VERSION_RE.match(left_part + "0"):
            raise InvalidVersion("version string %s is not a valid glob version" \
                                 % version_string)
        if not left_part.endswith("."):
            raise InvalidVersion("version string %s is not a valid glob version" \
                                 % version_string)

        # discart the last dot
        left_part = left_part[:-1]
        parts = left_part.split(".")
        if len(parts) < 1 or len(parts) > 3:
            raise InvalidVersion("version string %s is not a valid glob version" \
                                 % version_string)

        left = GEQ(".".join(parts + ["0"] * (3 - len(parts))))
        parts[-1] = str(int(parts[-1]) + 1)
        right = LT(".".join(parts + ["0"] * (3 - len(parts))))
        return left, right

class RawRequirementParser(object):
    """A simple parser for requirement strings."""
    def __init__(self):
        self._scanner = _DEFAULT_SCANNER

    def tokenize(self, requirement_string):
        scanned, remaining = self._scanner.scan(requirement_string)
        if len(remaining) > 0:
            raise DepSolverError("Invalid requirement string: %r" % requirement_string)
        else:
            return iter(scanned)

    def parse(self, requirement_string):
        parsed = OrderedDict()

        def _parse_full_block(requirement_block):
            distribution, operator, version = requirement_block
            if _is_glob_version(version.value):
                if not isinstance(operator, EqualToken):
                    raise InvalidVersion("glob version %s can only be use with == operation" \
                            % version.value)
                else:
                    if not distribution.value in parsed:
                        parsed[distribution.value] = []
                    parsed[distribution.value].extend(_glob_version_to_constraints(version.value))
            else:
                if not distribution.value in parsed:
                    parsed[distribution.value] = []
                parsed[distribution.value].append(_spec_factory(operator)(version.value))

        tokens_stream = self.tokenize(requirement_string)
        for requirement_block in iter_over_requirement(tokens_stream):
            if len(requirement_block) == 3:
                _parse_full_block(requirement_block)
            elif len(requirement_block) == 2:
                distribution = requirement_block[0]
                if not isinstance(requirement_block[1], AnyToken):
                    raise DepSolverError("Invalid requirement block: %s" % requirement_block)
                if not distribution.value in parsed:
                    parsed[distribution.value] = []
                parsed[distribution.value].append(Any())
            elif len(requirement_block) == 1:
                distribution = requirement_block[0]
                if not distribution.value in parsed:
                    parsed[distribution.value] = []
                parsed[distribution.value].append(Any())
            else:
                raise DepSolverError("Invalid requirement block: %s" % requirement_block)

        return parsed
