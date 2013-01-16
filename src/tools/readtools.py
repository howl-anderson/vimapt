#!/usr/bin/env python
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
vim_home = './test'
input_file = 'apttest.vpb'
fd = open(input_file, 'r')
fd_stream = fd.read()
meta_stream, package_stream = fd_stream.split('\n\n', 1)
meta_data = load(meta_stream, Loader=Loader)
print meta_data
print "@@@@@@@@@@@@"
print package_stream

meta_control_absdir = os.path.join(vim_home, 'vimapt/control')
meta_control_abspath_file = os.path.join(meta_control_absdir, meta_data['control']['source'])
if not os.path.isdir(meta_control_absdir):
    os.makedirs(meta_control_absdir)
fd = open(meta_control_abspath_file , 'w')
meta_control_stream = dump(meta_data['control'], Dumper=Dumper)
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
    package_absdir = os.path.join(vim_home, package_dir)
    package_abspath_file = os.path.join(vim_home, file)
    if not os.path.isdir(package_absdir):
        os.makedirs(package_absdir)
    fd = open(package_abspath_file, 'w')
    fd.write(file_stream)
    fd.close()
    start_point += filelines
print package_data
