#!/usr/bin/env python

import os

from vimapt import RemoteRepo


def make_index(work_dir):
    repo_object = RemoteRepo.RemoteRepo(work_dir)
    repo_object.make_package_index()


def main():
    make_index(os.getcwd())


if __name__ == "__main__":
    main()
