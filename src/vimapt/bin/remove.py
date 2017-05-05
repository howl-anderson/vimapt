#!/usr/bin/env python

import sys

from vimapt import Remove


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    remove = Remove.Remove(vim_dir)
    remove.remove_package(package_name)
    print("Remove Succeed!")


if __name__ == "__main__":
    main()
