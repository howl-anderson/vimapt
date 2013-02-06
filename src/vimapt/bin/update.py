#!/usr/bin/env python

import sys
from vimapt import LocalRepo


def main():
    vim_dir = sys.argv[1]
    try:
        repo = LocalRepo.LocalRepo(vim_dir)
        repo.update()
    except Exception, e:
        print "Error:", e
        print "Update Failed!"
    else:
        print "Update Succeed!"


if __name__ == "__main__":
    main()
