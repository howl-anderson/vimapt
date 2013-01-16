#!/usr/bin/env python
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
#stream = """
#- [plugin/apttest.vim, 3]
#- [doc/apttest, 5]
#"""
#data = load(stream, Loader=Loader)
package_data = []
input_file = ['plugin/apttest.vim', 'doc/apttest.txt']
package_content = []
for file in input_file:
    fd = open(file, 'r')
    lines = fd.readlines()
    line_number = len(lines)
    package_content += lines
    fd.close()
    package_data.append([file, line_number])
#package_data = [['plugin/apttest.vim',5], ['doc/apttest',9]]
control_data = {'source':'apttest', 'section':'', 'version':'0.1', 'depends':''}
copyright_data = {'author':'apttest', 'maintiner':'', 'license':''}
data = {'package':package_data, 'control': control_data, 'copyright':copyright_data}
output = dump(data, Dumper=Dumper)
print output + "\n" + "".join(package_content),
