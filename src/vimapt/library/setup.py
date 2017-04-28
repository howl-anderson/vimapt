from distutils.core import setup
from setuptools import find_packages

setup(
    name='vimapt',
    version='0.1',
    install_requires=[
        'pyyaml',
        'six',
        'semantic_version',
        'requirements-parser'
    ],
    packages=find_packages(exclude=[]),
    url='www.vimapt.org',
    license='GPL',
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',
    description='APT-like package manager for Vim'
)
