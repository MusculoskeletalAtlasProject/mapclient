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
import logging
import tempfile

from PySide2 import QtCore
from mapclient.settings.definitions import INTERNAL_WORKFLOWS_DIR

from mapclient.settings.info import VERSION_STRING


def get_data_directory():
    """
    Return the directory where we can store data for the application.
    Like settings and log files etc.
    """
    settings = QtCore.QSettings()
    fn = settings.fileName()
    app_dir, _ = os.path.splitext(fn)

    return app_dir


def _get_app_directory(name):
    app_dir = get_data_directory()
    name_dir = os.path.join(app_dir, name)

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    return name_dir


def get_virtualenv_directory():
    return _get_app_directory('venv_' + VERSION_STRING)


def get_default_internal_workflow_dir():
    return os.path.join(tempfile.gettempdir(), INTERNAL_WORKFLOWS_DIR)


def get_virtualenv_site_packages_directory(virtualenv_dir):
    print('Confirm path on other OSes, so far only checked on Windows.')
    return os.path.join(virtualenv_dir, 'Lib', 'site-packages')


def get_log_directory():
    return _get_app_directory('logs')


def get_log_location():
    """
    Set up location where log files will be stored (platform dependent).
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        for i in range(len(logger.handlers)):
            if isinstance(logger.handlers[i], logging.handlers.RotatingFileHandler):
                return logger.handlers[i].baseFilename

    log_filename = 'logging_record.log'
    log_directory = get_log_directory()
    logging_file_location = os.path.join(log_directory, log_filename)

    return logging_file_location


def get_configuration_suffix():
    return '.conf'


def get_configuration_file(location, identifier):
    if 'src/mapclient' in location:
        raise Exception('Saving this in the wrong place.')

    return os.path.join(location, identifier + get_configuration_suffix())


DISPLAY_FULL_PATH = 'AIJDKUUGCNEGELND'


def get_configuration(option):
    if option == DISPLAY_FULL_PATH:
        return False


