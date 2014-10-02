#!/usr/bin/env python

import sys
from vimapt import Remove

import traceback


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    try:
        remove = Remove.Remove(package_name, vim_dir)
        remove.remove_package()
    except Exception, e:
        print "Error:", e, traceback.format_exc()
        print "Remove Failed!"
    else:
        print "Remove Succeed!"

if __name__ == "__main__":
    main()