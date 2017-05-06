from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vimapt-tools',

    version='0.1.0',

    include_package_data=True,

    description='CLI tools for vimapt',
    long_description=long_description,

    # The project's main homepage.
    url='https://www.vimapt.org',

    # Author details
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',

    packages=find_packages(exclude=[]),

    install_requires=['vimapt_library'],

    entry_points={
        'console_scripts': [
            'vimapt-makevpb=vimapt_tools.makevpb:main',
            'vimapt-maketpl=vimapt_tools.maketpl:main',
            'vimapt-makepool=vimapt_tools.makepool:main',
            'vimapt-makeindex=vimapt_tools.makeindex:main'
        ],
    },
)