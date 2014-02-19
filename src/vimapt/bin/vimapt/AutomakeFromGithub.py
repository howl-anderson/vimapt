#!/usr/bin/env python

import tempfile
import subprocess
import sys
import os
import shutil
from vimapt import Compress
from vimapt import Extract  

class AutomakeFromGithub:
    def __init__(self, user_name, plugin_name):
        self.version = "1.0"
        self.revision = "1"
        #self.work_dir = tempfile.mkdtemp("vimapt-from-github")
        self.user_name = user_name
        self.plugin_name = plugin_name
        #self.build_dir = "/".join([self.work_dir, "_".join(["-".join(["github", self.user_name, self.plugin_name]), "1.0-1"])])
        self.pkg_name = "github-" + user_name + "-" + plugin_name # TODO
        self.build_dir = "_".join(["-".join(["github", self.user_name, self.plugin_name]), "1.0-1"]) # path like: github-user-plugin_1.0-1
        self.work_dir = tempfile.mkdtemp(self.build_dir)
        print self.work_dir
        self.github_url = "".join(["https://github.com/", self.user_name, "/", self.plugin_name, ".git"])
        subprocess.call(["git", "clone", "--depth", "1", self.github_url, self.work_dir])

    def remove_dot_git_dir(self):
        dot_git_dir = os.path.join(self.work_dir, ".git")
        shutil.rmtree(dot_git_dir)

    def build_package_struct(self):
        obj = Extract.Extract('vimapt.vpb', self.work_dir)
        obj.extract()

        rel_tpl_list = ['vimapt/control/vimapt.yaml',                           
                        'vimapt/copyright/vimapt.yaml',                         
                        'vimrc/vimapt.vimrc',] 

        for rel_tpl_file in rel_tpl_list:                                       
            tpl_file = os.path.join(self.work_dir, rel_tpl_file)          
            tpl_file_dir = os.path.dirname(tpl_file)                            
            _, ext_name = os.path.splitext(tpl_file)                            
            target_file = os.path.join(tpl_file_dir, self.pkg_name + ext_name)   
            print tpl_file                                                      
            print target_file                                                   
            os.rename(tpl_file, target_file)  

    def build_package(self):
        full_version = self.version + "-" + self.revision
        self.full_pkg_name = self.pkg_name + "_" + full_version + ".vpb"
        self.target_file = self.full_pkg_name # TODO
        compress_object = Compress.Compress(self.work_dir, self.target_file)
        compress_object.compress()

    def report_package_path(self):
        return self.target_file


if __name__ == "__main__":
    user_name = sys.argv[1]
    plugin_name = sys.argv[2]
    obj = AutomakeFromGithub(user_name, plugin_name)
    obj.remove_dot_git_dir()
    obj.build_package_struct()
    obj.build_package()
    print obj.report_package_path()
