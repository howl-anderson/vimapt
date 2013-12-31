#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
from setuptools import setup
from setuptools import find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="vimapt",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.vpb']},

    description="a vim package manager just like debian's apt",
    long_description=read('README'),
    author="howlanderson",
    author_email="u1mail2me@gmail.com",

    license="GPL",
    keywords="vimapt vim plugin",
    platforms="Independant",
    url="http://howlanderson.bitbucket.org",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL License",
        ],
)
