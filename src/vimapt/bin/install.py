#!/usr/bin/env python

import sys
#import traceback
from vimapt import Install

def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    try:
        install = Install.Install(vim_dir)
        install.repo_install(package_name)
    except Exception, e:
        print "Error:", e
        #traceback.print_exc()
        print "Install Failed!",
    else:
        print "Install Succeed!",


if __name__ == "__main__":
    main()
