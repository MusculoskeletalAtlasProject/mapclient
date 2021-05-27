#!/usr/bin/env python

import codecs
import os
import re

from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Define the list of requirements
install_requires = [
    'PySide2',
]


setup(
    name='mapclientplugins.builtin',
    version=find_version("mapclient", "settings", "version.py"),
    description='Builtin plugins for MAP Client.',
    author='MAP Client Developers',
    author_email='mapclient-devs@physiomeproject.org',
    url='https://github.com/MusculoskeletalAtlasProject/mapclient',
    namespace_packages=['mapclientplugins', ],
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'tests.*', 'mapclient', 'mapclient.*', 'utils', 'utils.*' ]),
    install_requires=install_requires,
)
