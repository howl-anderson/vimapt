#!/usr/bin/env python
import os
import sys
import shutil
import errno

package_name = raw_input("input you package name:\n")
package_version = raw_input("input you package version, format like x.y.z:\n")
print package_name
print package_version
work_dir = '.'
tpl_dir = './tpl'
package_dir = package_name + '-' + package_version
package_dir_abspath = os.path.join(work_dir, package_dir)
if os.path.isdir(package_dir_abspath):
    rm_exists_dir = raw_input("Dir " + package_dir_abspath + " exists, should i remove it? (y,n):\n")
    if rm_exists_dir == "y":
        shutil.rmtree(package_dir_abspath)
        print "package dir remove successed!"
    else:
        print "package exists and user aborted this process, exit!"
        sys.exit(0)


def copy_dir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

copy_dir(tpl_dir, package_dir_abspath)
print "new packaging dir build in ", package_dir_abspath
package_control_path = os.path.join(package_dir_abspath, 'vimapt/control')
package_copyright_path = os.path.join(package_dir_abspath, 'vimapt/copyright')

os.rename(os.path.join(package_control_path, 'vimapt'), os.path.join(package_control_path, package_name))
os.rename(os.path.join(package_copyright_path, 'vimapt'), os.path.join(package_copyright_path, package_name))
print "have fun!"
