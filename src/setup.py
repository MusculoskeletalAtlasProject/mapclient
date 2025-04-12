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


with open('README.rst') as f:
    readme = f.read()

# Define the list of requirements
package_dependencies = [
    'PySide6 >= 6.5, != 6.7.0',
    'rdflib',
    'virtualenv',
    'requests',
    'python-dateutil',
    'dulwich != 0.22.0',
    'pmr2.wfctrl >= 0.6.0',
    'pmr2.client >= 0.2',
    'packaging',
    'filelock',
    'psutil >= 6.0',
    'PyGithub',
    'numpy',
]

extras_require = {
    'dev': [
        'PyInstaller',
    ]
}

packages = find_packages(exclude=['tests', 'tests.*', 'mapclientplugins', 'mapclientplugins.*', 'utils', 'utils.*'])
packages.append('mapclient.tools.pluginwizard.qt.images')

setup(
    name='mapclient',
    version=find_version("mapclient", "settings", "version.py"),
    description='A framework for managing and sharing workflows.',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='MAP Client Developers',
    author_email='mapclient-devs@physiomeproject.org',
    url='https://github.com/MusculoskeletalAtlasProject/mapclient',
    # namespace_packages=['mapclientplugins', ],
    packages=packages,
    package_data={'mapclient.tools.annotation': ['annotation.voc'], 'mapclient.tools.osxapp': ['mapclient.icns'],
                  'mapclient.tools.pluginwizard.qt.images':
                      ['data-sink.png', 'data-source.png', 'default.png', 'fitting.png', 'image-processing.png',
                       'model-viewer.png', 'morphometric.png', 'registration.png', 'segmentation.png', 'utility.png']},
    # py_modules=['mapclient.mapclient'],
    include_package_data=True,
    entry_points={
        'gui_scripts': ['mapclient=mapclient.application:main'],
        'console_scripts': ['mapclient_sans_gui=mapclient.application:sans_gui_main',
                            'mapclient_use=mapclient.application:user_specified_environment_main',
                            ],
    },
    install_requires=package_dependencies,
    extras_require=extras_require,
)
