#!/usr/bin/env python

import install

def install_local_file(file_path, target_dir):
    install.extract(file_path, target_dir)

def main():
    target_dir = '~/.vim/'
    file_path = 'test-0.3.vpb'
    install_local_file(file_path, target_dir)

if __name__ == "__main__":
    pass
