import sys

if sys.version_info[:1] < (2, 7):
    from ._collections import OrderedDict

    def sorted_with_cmp(x, cmp):
        return sorted(x, cmp=cmp)
else:
    from collections import OrderedDict

    from functools import cmp_to_key
    def sorted_with_cmp(x, cmp):
        return sorted(x, key=cmp_to_key(cmp))

from ._itertools import izip_longest
