#!/usr/bin/env python

import sys
import os
#import traceback
from vimapt import Extract
from vimapt import AutomakeFromGithub

def main():
    vim_dir = sys.argv[1]
    user_name = sys.argv[2]
    plugin_name = sys.argv[3]
    try:
        obj = AutomakeFromGithub.AutomakeFromGithub(user_name, plugin_name)
        obj.remove_dot_git_dir()
        obj.build_package_struct()
        obj.build_package()
        package_file = obj.report_package_path()
        package_file_fullpath = os.path.join(vim_dir, "vimapt/bin", package_file)
        obj = Extract.Extract(package_file_fullpath, vim_dir)
        obj.extract()
    except Exception, e:
        print "Error:", e
        #traceback.print_exc()
        print "Github Install Failed!",
    else:
        print "Github Install Succeed!",


if __name__ == "__main__":
    main()
