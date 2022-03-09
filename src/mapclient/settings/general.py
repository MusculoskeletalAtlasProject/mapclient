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
import sys

import json

import psutil
from filelock import FileLock

from PySide2 import QtCore

from mapclient.core.exitcodes import LOG_FILE_LOCK_FAILED
from mapclient.settings.definitions import INTERNAL_WORKFLOWS_DIR, PID_DATABASE_FILE_NAME

from mapclient.settings.info import VERSION_STRING


def get_data_directory():
    """
    Return the directory where we can store data for the application.
    Like settings and log files etc.
    """
    settings = QtCore.QSettings()
    fn = settings.fileName()

    return os.path.dirname(fn)


def _get_app_directory(name):
    app_dir = get_data_directory()
    name_dir = os.path.join(app_dir, name)

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    return name_dir


def get_virtualenv_directory():
    return _get_app_directory('venv_' + VERSION_STRING)


def get_default_internal_workflow_dir():
    return _get_app_directory(INTERNAL_WORKFLOWS_DIR)


def get_virtualenv_site_packages_directory(virtualenv_dir):
    print('Confirm path on other OSes, so far only checked on Windows.')
    return os.path.join(virtualenv_dir, 'Lib', 'site-packages')


def get_log_directory():
    return _get_app_directory('logs')


def _get_pid_database_file():
    return os.path.join(get_data_directory(), PID_DATABASE_FILE_NAME)


def get_log_location():
    """
    Return the location of the log file that is associated with the current MAP Client instance. If the current instance has not been
    assigned a log file, a new log file will be created and assigned to the current PID.
    """
    log_directory = get_log_directory()
    database_file = _get_pid_database_file()

    try:
        # If the user experiences a hardware crash during the execution of this block, it is possible that the lockfile will remain
        # possessed by a dead process. If this happens, the user will have to manually delete the lockfile.
        lock = FileLock(database_file + ".lock", 3)
        with lock:
            try:
                with open(database_file, "r") as file:
                    database = json.loads(file.read())
            except IOError:
                database = []

            # Check if the current PID has already been assigned to a log file. If not, assign it to a new log file.
            current_pid = os.getpid()
            index = -1
            for i in range(len(database)):
                if int(database[i][0]) == current_pid:
                    index = i
                    break
            if index == -1:
                index = assign_log_file(database_file, database, current_pid)

    except TimeoutError:
        sys.exit(LOG_FILE_LOCK_FAILED)

    log_filename = 'logging_record_' + str(index) + '.log'
    logging_file_location = os.path.join(log_directory, log_filename)

    return logging_file_location


def assign_log_file(database_file, database, current_pid):
    unassigned_indices = []
    for i in range(len(database)):
        if database[i] == -1:
            unassigned_indices.append(i)
        else:
            pid = int(database[i][0])
            if not psutil.pid_exists(pid):
                database[i] = [-1, []]
                unassigned_indices.append(i)

    while database and database[-1][0] == -1:
        database.pop()

    max_index = len(database)
    unassigned_indices.append(max_index)
    index = min(unassigned_indices)

    if index < max_index:
        database[index] = [current_pid, []]
    else:
        database.append([current_pid, []])

    with open(database_file, "w") as file:
        file.write(json.dumps(database))

    return index


def get_pid_database():
    database_file = _get_pid_database_file()

    try:
        with open(database_file, "r") as file:
            database = json.loads(file.read())
    except IOError:
        database = []

    return database


def set_pid_database(database):
    database_file = _get_pid_database_file()

    try:
        lock = FileLock(database_file + ".lock", 3)
        with lock:
            with open(database_file, "w") as file:
                file.write(json.dumps(database))

    except TimeoutError:
        sys.exit(LOG_FILE_LOCK_FAILED)


def get_restricted_plugins():
    """
    Returns a set of MAP plugins names. This set identifies the plugins already in use by other instances of the MAP Client.
    """
    database = get_pid_database()

    current_pid = os.getpid()
    restricted_plugins = set()
    for i in range(len(database)):
        if database[i][0] == current_pid:
            continue

        restricted_plugins = restricted_plugins | set(database[i][1])

    return restricted_plugins


# TODO: Add a list of known MAP plugins that need not be restricted (e.g., TRC Reader, etc).
def restrict_plugins(plugins):
    """
    Takes a set of plugins as input. Adds this set to the MAP PID database file. This is so that other instances of the MAP Client
    can see what plugins this instance is currently using.
    """
    database = get_pid_database()

    current_pid = os.getpid()
    for i in range(len(database)):
        if database[i][0] == current_pid:
            database[i][1] = list(plugins)

    set_pid_database(database)


def unrestrict_plugins():
    restrict_plugins(set())


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


