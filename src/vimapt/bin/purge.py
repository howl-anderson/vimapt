#!/usr/bin/env python

import sys

from vimapt import Purge


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]

    purge = Purge.Purge(vim_dir)
    purge.purge_package(package_name)
    print("Purge Succeed!")


if __name__ == "__main__":
    main()
