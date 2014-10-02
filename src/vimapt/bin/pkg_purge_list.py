#!/usr/bin/env python

import os
import sys
import vim


def main():
    vim_dir = sys.argv[1]
    install_dir = os.path.join(vim_dir, 'vimapt/install')
    install_file_list = [f for f in os.listdir(install_dir)
                         if os.path.isfile(os.path.join(install_dir, f))]
    remove_dir = os.path.join(vim_dir, 'vimapt/remove')
    remove_file_list = [f for f in os.listdir(remove_dir)
                        if os.path.isfile(os.path.join(remove_dir, f))]
    file_list = remove_file_list + install_file_list
    return file_list


if __name__ == "__main__":
    package_list = main()
    pkg_list_string = "[" + ",".join(["'" + i + "'" for i in package_list ]) + "]"
    vim.command('let s:package_purge_list = ' + pkg_list_string)
