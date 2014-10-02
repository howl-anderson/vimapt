#!/usr/bin/env python

import os
import sys
import vim
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def main():
    vim_dir = sys.argv[1]
    cache_dir = os.path.join(vim_dir, 'vimapt/cache')
    local_package_index_path = os.path.join(cache_dir, 'index/package')
    fd = open(local_package_index_path)
    source_stream = fd.read()
    fd.close()
    source_data = load(source_stream, Loader=Loader)
    package_name_list = source_data.keys()
    return package_name_list


if __name__ == "__main__":
    package_list = main()
    pkg_list_string = "[" + ",".join(["'" + i + "'" for i in package_list]) + "]"
    vim.command('let s:package_list = ' + pkg_list_string)
