#!/usr/bin/env python

import os

import sys
import vim


def main():
    vim_dir = sys.argv[1]
    install_dir = os.path.join(vim_dir, 'vimapt/install')
    file_list = []

    for f in os.listdir(install_dir):
        if os.path.isfile(os.path.join(install_dir, f)) and not os.path.basename(f).startswith('.'):
            file_list.append(f)

    return file_list


if __name__ == "__main__":
    package_list = main()

    # set vim's variable to make command complete function works
    pkg_list_string = "[" + ",".join(["'" + i + "'" for i in package_list]) + "]"
    vim.command('let s:package_remove_list = ' + pkg_list_string)
