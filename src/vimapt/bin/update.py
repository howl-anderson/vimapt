#!/usr/bin/env python

import sys

from vimapt import LocalRepo


def main():
    vim_dir = sys.argv[1]
    repo = LocalRepo.LocalRepo(vim_dir)
    repo.update()
    print("Update Succeed!")


if __name__ == "__main__":
    main()
