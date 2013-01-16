#!/usr/bin/env python

import os
import tempfile
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def extract(input_file, output_dir):
    fd = open(input_file, 'r')
    file_stream = fd.read()
    meta_stream, package_stream = file_stream.split('\n\n', 1)
    meta_data = load(meta_stream, Loader=Loader)
    package_lines = package_stream.split('\n')


    package_data = {}
    start_point = 0
    for file, filelines in meta_data['package']:
        print file, filelines
        print start_point
        end_point =  start_point + filelines
        list_data = package_lines[start_point:end_point]
        file_stream = "\n".join(list_data)
        package_data[file] = file_stream
        package_dir = os.path.dirname(file)
        package_absdir = os.path.join(output_dir, package_dir)
        package_abspath_file = os.path.join(output_dir, file)
        if not os.path.isdir(package_absdir):
            os.makedirs(package_absdir)
        fd = open(package_abspath_file, 'w')
        fd.write(file_stream)
        fd.close()
        start_point += filelines

def get_plugin_name(file_name):
    plugin_name, _ = file_name.split('-', 1)
    return plugin_name

def get_depends():
    pass

def check_depends(tmp_dir, plugin_name):
    meta_control_relpath = 'vimapt/copyright' + plugin_name
    meta_control_abspath = os.path.join(tmp_dir, meta_control_relpath)
    fd = open(meta_control_abspath , 'w')
    meta_control_stream = fd.read() 
    meta_control_data = load(meta_control_stream, Loader=Loader)
    fd.write(meta_control_stream)
    fd.close()
    
    meta_copyright_absdir = os.path.join(vim_home, 'vimapt/copyright')
    meta_copyright_abspath_file = os.path.join(meta_copyright_absdir, meta_data['control']['source'])
    if not os.path.isdir(meta_copyright_absdir):
        os.makedirs(meta_copyright_absdir)
    fd = open(meta_copyright_abspath_file , 'w')
    meta_copyright_stream = dump(meta_data['copyright'], Dumper=Dumper)
    fd.write(meta_copyright_stream)
    fd.close()

def main():
    input_file = 'test-0.3.vpb'
    #output_dir = tempfile.mkdtemp()
    output_dir = 'testdir'
    extract(input_file, output_dir)
    #plugin_name = get_plugin_name(input_file)
    #check_depends(tmp_dir, plugin_name)

if __name__ == "__main__":
    main()
