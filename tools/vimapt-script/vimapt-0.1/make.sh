#!/bin/bash

rm ../vimapt_0.1.orig.tar.gz
python setup.py bdist_egg
dh_make --createorig
debuild
sudo apt-get purge python-vimapt
sudo dpkg -i ../python-vimapt_0.1-1_all.deb
