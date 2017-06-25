#!/usr/bin/env python

import sys

from vimapt import Upgrade


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]

    remove = Upgrade.Upgrade(vim_dir)
    remove.upgrade_package(package_name)
    print("Upgrade Succeed!")


if __name__ == "__main__":
    main()
