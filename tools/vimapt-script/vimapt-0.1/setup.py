#!/usr/bin/env python
#-*- coding:utf8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name="vimapt",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.vpb']},

    description="a vim package manager just like debian's apt",
    long_description="vimapt is a vim package manager. vimapt's command and function are very like to debian's apt, so it called vim's apt",
    author="howlanderson",
    author_email="u1mail2me@gmail.com",

    license="GPL",
    keywords="vimapt vim plugin",
    platforms="Independant",
    url="http://www.howlanderson.net",
)
