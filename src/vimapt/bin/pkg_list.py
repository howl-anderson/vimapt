#!/usr/bin/env python

import os
import sys

import vim

from vimapt.data_format import loads


def main():
    vim_dir = sys.argv[1]
    cache_dir = os.path.join(vim_dir, 'vimapt/cache')
    local_package_index_path = os.path.join(cache_dir, 'index/package')

    with open(local_package_index_path) as fd:
        source_stream = fd.read()

    source_data = loads(source_stream)
    package_name_list = source_data.keys()
    return package_name_list


if __name__ == "__main__":
    package_list = main()
    pkg_list_string = "[" + ",".join(["'" + i + "'" for i in package_list]) + "]"
    vim.command('let s:package_list = ' + pkg_list_string)
