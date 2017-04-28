# -*- coding: utf-8 -*-
import sys

from vimapt import Install
from vimapt.exception import VimaptAbortOperationException


def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    install = Install.Install(vim_dir)
    try:
        install.repo_install(package_name)
    except VimaptAbortOperationException as e:
        print(e)
    else:
        print("Install Succeed!")


if __name__ == "__main__":
    main()
