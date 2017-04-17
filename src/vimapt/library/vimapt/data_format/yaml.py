from __future__ import absolute_import

import functools

from yaml import dump, Dumper, load, Loader

dumps = functools.partial(dump, Dumper=Dumper)
loads = functools.partial(load, Loader=Loader)

__all__ = ['dumps', 'loads']
