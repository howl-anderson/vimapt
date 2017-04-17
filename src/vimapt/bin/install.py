#!/usr/bin/env python

import sys

from vimapt import Install


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    install = Install.Install(vim_dir)
    install.repo_install(package_name)
    print("Install Succeed!")


if __name__ == "__main__":
    main()
