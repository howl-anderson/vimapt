#!/bin/bash

rm vimapt-tools_*
cd vimapt-tools-0.1
dh_make --createorig
debuild
cd ..
sudo apt-get purge vimapt-tools
sudo dpkg -i vimapt-tools_0.1-1_all.deb
