"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
import os

from PySide import QtCore

from mapclient.settings.info import VERSION_STRING

def getDataDirectory():
    """
    Return the directory where we can store data for the application.
    Like settings and log files etc.
    """
    settings = QtCore.QSettings()
    fn = settings.fileName()
    app_dir, _ = os.path.splitext(fn)

    return app_dir


def _getAppDirectory(name):
    app_dir = getDataDirectory()
    name_dir = os.path.join(app_dir, name)

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    return name_dir


def getVirtEnvDirectory():
    return _getAppDirectory('venv_' + VERSION_STRING)


def getVirtualEnvSitePackagesDirectory(virtualenv_dir):
    print('Confirm path on other OSes, so far only checked on Windows.')
    return os.path.join(virtualenv_dir, 'Lib', 'site-packages')


def getLogDirectory():
    return _getAppDirectory('logs')


def getLogLocation():
    """
    Set up location where log files will be stored (platform dependent).
    """
    log_filename = 'logging_record.log'
    log_directory = getLogDirectory()

    logging_file_location = os.path.join(log_directory, log_filename)

    return logging_file_location


def getConfigurationSuffix():
    return '.conf'


def getConfigurationFile(location, identifier):
    if 'src/mapclient' in location:
        raise Exception('Saving this in the wrong place.')

    return os.path.join(location, identifier + getConfigurationSuffix())


DISPLAY_FULL_PATH = 'AIJDKUUGCNEGELND'


def getConfiguration(option):
    if option == DISPLAY_FULL_PATH:
        return False


