#!/usr/bin/env python

import sys

from vimapt import Upgrade


def main():
    vim_dir = sys.argv[1]

    upgrador = Upgrade.Upgrade(vim_dir)
    upgrador.upgrade_all()
    print("Upgrade Succeed!")


if __name__ == "__main__":
    main()
