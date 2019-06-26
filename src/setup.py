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
install_requires = ['PySide2',
                    'rdflib',
                    'virtualenv',
                    'requests',
                    'python-dateutil',
                    'dulwich',
                    'pmr2.client']


setup(
    name='mapclient',
    version=find_version("mapclient", "settings", "version.py"),
    description='A framework for managing and sharing workflows.',
    author='MAP Client Developers',
    author_email='mapclient-devs@physiomeproject.org',
    url='https://github.com/MusculoskeletalAtlasProject/mapclient',
    # namespace_packages=['mapclientplugins', ],
    packages=find_packages(exclude=['tests', 'tests.*', 'mapclientplugins', 'mapclientplugins.*', 'utils', 'utils.*' ]),
    package_data={'mapclient.tools.annotation': ['annotation.voc'], 'mapclient.tools.osxapp': ['mapclient.icns']},
    # py_modules=['mapclient.mapclient'],
    entry_points={'console_scripts': ['mapclient=mapclient.application:main']},
    install_requires=install_requires,
)
