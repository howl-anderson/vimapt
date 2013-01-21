#!/usr/bin/env python

import os
import sys

def install_package(package_name):
    pass

def main():
    vim_dir = sys.argv[1]
    package_name = sys.argv[2]
    repo = LocalRepo.LocalRepo(vim_dir)
    repo.update()
    package_path = repo.get_package(package_name)
    print package_path
    install.extract(package_path, vim_dir)

if __name__ == "__main__":
    print sys.argv
    current_file_path = os.path.dirname(sys.argv[3])
    sys.path.append(current_file_path) 
    print sys.path
    
    import LocalRepo
    import install
    main()
