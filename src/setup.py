#!/usr/bin/env python
import platform, sys, os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop

# Version, this should match the value in mapclient.settings.info
version = '0.12.0'
# Define the list of requirments
install_requires = ['rdflib',
                    'virtualenv',
                    'python-dateutil',
                    'pmr2.wfctrl',
                    'pmr2.client']
try:
    import PySide
    pyside_version = PySide.__version__
    pyside_requirement = 'PySide==' + pyside_version
    # PySide version 1.1.0 is not known about by PyPi
    # but it will work for the MAP Client software
    if pyside_version != '1.1.0':
        pyside_requirement = None
except ImportError:
    # If we don't have PySide we will need to build it
    pyside_requirement = 'PySide'

if pyside_requirement is not None:
    install_requires.append(pyside_requirement)

try:
    import importlib
except ImportError:
    # Python < 2.7 doesn't have importlib in the core distribution
    install_requires.append('importlib')

def createApplication(install_dir):
    from subprocess import call
    call([sys.executable, 'shimbundle.py', 'MAP Client', version],
          cwd=os.path.join(install_dir, 'mapclient', 'tools', 'osxapp'))

# For OS X we want to install MAP Client into the Applications directory
class install(_install):

    def run(self):
        _install.run(self)
        mac_release, _, _ = platform.mac_ver()
        if  mac_release:
            self.execute(createApplication, (self.install_lib,),
                         msg="Creating OS X Application")


# For OS X we want to install MAP Client into the Applications directory
class develop(_develop):

    def run(self):
        _develop.run(self)
        mac_release, _, _ = platform.mac_ver()
        if  mac_release:
            self.execute(createApplication, (self.setup_path,),
                         msg="Creating OS X Application")


setup(name='mapclient',
     version=version,
     description='A framework for managing and sharing workflows.',
     author='MAP Client Developers',
     author_email='mapclient-devs@physiomeproject.org',
     url='https://launchpad.net/mapclient',
     namespace_packages=['mapclient', ],
     packages=find_packages(exclude=['tests', 'tests.*', ]),
     package_data={'mapclient.tools.annotation': ['annotation.voc'], 'mapclient.tools.osxapp': ['mapclient.icns']},
     # py_modules=['mapclient.mapclient'],
     entry_points={'console_scripts': ['mapclient=mapclient.application:winmain']},
     install_requires=install_requires,
     cmdclass={'install': install, 'develop': develop}
)
