#!/usr/bin/env python

import sys
from vimapt import Purge


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    try:
        purge = Purge.Purge(package_name, vim_dir)
        purge.purge_package()
    except Exception, e:
        print "Error:", e
        print "Purge Failed!"
    else:
        print "Purge Succeed!"

if __name__ == "__main__":
    main()
