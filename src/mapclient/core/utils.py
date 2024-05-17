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
import logging
import os
import pathlib
import re
import shutil
import sys
from pathlib import Path

from subprocess import Popen, PIPE, DEVNULL
import PySide6 as RefMod

from mapclient.settings.definitions import APPLICATION_NAME, PLUGINS_PACKAGE_NAME
from mapclient.settings.general import get_configuration_file

logger = logging.getLogger(__name__)


def is_frozen():
    return getattr(sys, 'frozen', False)


def is_mapping_tools():
    variant = get_map_client_variant()
    return variant == "mapping-tools"


def get_map_client_variant():
    application_name = os.path.basename(sys.executable)
    pattern = r'{}-(.*).exe'.format(APPLICATION_NAME)
    match = re.search(pattern, application_name)
    variant = match.group(1) if match else ""

    return variant


def convert_exception_to_message(e):
    string_e = str(e)
    return string_e.replace('\n', ' ')


def get_system_pip_candidates():
    """Return a list of strings with the candidates for the pip application
    for this environment.
    """
    if sys.version_info < (3, 0):
        pip_candidates = ['pip', 'pip2']
    else:
        pip_candidates = ['pip', 'pip3']

    return pip_candidates


def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, permissions):
        return (os.path.exists(fn) and os.access(fn, permissions)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if sys.platform == "win32":
            # PATHEXT is necessary to check on Windows.
            pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            files = [cmd]
        for name in files:
            if _access_check(name, mode):
                return name

        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for directory in path:
        normdir = os.path.normcase(directory)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(directory, thefile)
                if _access_check(name, mode):
                    return name

    return None


def load_configuration(location, identifier):
    filename = get_configuration_file(location, identifier)
    configuration = '{}'
    try:
        with open(filename) as f:
            configuration = f.read()
    except Exception:
        pass
    return configuration


def copy_step_additional_config_files(step, source_configuration_dir, target_configuration_dir):
    additional_cfg_files = get_steps_additional_config_files(step)
    if len(additional_cfg_files):
        logger.info(f'Copying additional cfg files for: {step.getName()}')
    for additional_cfg_file in additional_cfg_files:
        logger.info(f' * Additional cfg file reported: {additional_cfg_file}')
        source_cfg_dir = os.path.dirname(additional_cfg_file)
        source_cfg_file = os.path.join(source_configuration_dir, additional_cfg_file)

        source_basename = os.path.basename(additional_cfg_file)
        source_workflow_relative_cfg = os.path.join(source_cfg_dir, source_basename)

        target_cfg_file = os.path.realpath(os.path.join(target_configuration_dir, source_workflow_relative_cfg))
        if os.path.isfile(source_cfg_file):
            required_path = os.path.join(target_configuration_dir, source_cfg_dir)
            if not os.path.exists(required_path):
                os.makedirs(required_path)
            logger.info(f' * Copying cfg file: {source_cfg_file} -> {target_cfg_file}')
            shutil.copyfile(source_cfg_file, target_cfg_file)
        else:
            logger.warning(f' * Did not find reported configuration file: {source_cfg_file}.')


def get_steps_additional_config_files(step):

    workflow_dir = step.getLocation()

    def _workflow_relative_path(filename):
        if os.path.isabs(filename):
            return pathlib.PureWindowsPath(os.path.normpath(os.path.relpath(filename, workflow_dir))).as_posix()

        return filename

    additional_config_files = step.getAdditionalConfigFiles()
    return [_workflow_relative_path(file) for file in additional_config_files]


class FileTypeObject(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

    def flush(self):
        pass


def grep(path, regex, one_only=False, file_endswith=''):
    re_obj = re.compile(regex)
    res = {}
    for root, dirs, fnames in os.walk(path):
        if '.git' in dirs:
            dirs.remove('.git')
        if '.hg' in dirs:
            dirs.remove('.hg')
        if '.svn' in dirs:
            dirs.remove('.svn')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for f_name in fnames:
            full_filename = os.path.join(root, f_name)
            if f_name.endswith(file_endswith) and not is_binary(full_filename):
                with open(full_filename) as f:
                    contents = f.readlines()
                    for line_no, line in enumerate(contents):
                        if re_obj.search(line):
                            relative_name = full_filename.replace(os.path.join(path, ''), '')
                            if relative_name not in res:
                                res[relative_name] = []

                            res[relative_name].append([line_no, line.rstrip()])
                            if one_only:
                                return res

    return res


def determine_step_name(step_name_file, class_name):
    r = r'[ \t]+super\(' + class_name + ', self\)\.__init__\(\'([^\']+)\', location\)'
    re_step_name = re.compile(r)

    step_name = None
    with open(step_name_file) as f:
        contents = f.readlines()
        for line in contents:
            search_result = re_step_name.search(line)
            if search_result:
                step_name = search_result.group(1)
                break

    return step_name


def determine_step_class_name(step_name_file):
    r = r'class[ \t]+([\w]+)\(\bWorkflowStepMountPoint\b\):'
    re_step_class = re.compile(r)

    step_class_name = None
    with open(step_name_file) as f:
        contents = f.readlines()
        for line in contents:
            search_result = re_step_class.search(line)
            if search_result:
                step_class_name = search_result.group(1)
                break

    return step_class_name


def determine_package_name(plugin_dir, file_in_package):
    plugin_package_path = os.path.join(plugin_dir, PLUGINS_PACKAGE_NAME)
    package_name = file_in_package.replace(plugin_package_path, '')
    package_name = package_name.split(os.path.sep)[0]
    return package_name


def convert_name_to_python_package(name):
    package_name = name.lower()
    package_name = package_name.replace(' ', '')
    return package_name + 'step'


def is_binary(filename):
    """Return true if the given filename is binary.

    :param filename: filename of the file to interrogate.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>
    @author: Hugh Sorby <h.sorby@auckland.ac.nz>"""
    with open(filename, 'rb') as fin:
        CHUNK_SIZE = 1024
        while 1:
            chunk = fin.read(CHUNK_SIZE)
            if b'\0' in chunk:  # found null byte
                return True
            if len(chunk) < CHUNK_SIZE:
                break  # done

    return False


def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)

    return None


def qt_tool_wrapper(qt_tool, args, external=False):
    pyside_dir = Path(RefMod.__file__).resolve().parent
    if external:
        exe = qt_tool
    elif sys.platform != "win32":
        exe = os.path.join(pyside_dir, "Qt", "libexec", qt_tool)
    else:
        exe = os.path.join(pyside_dir, qt_tool)

    cmd = [os.fspath(exe)] + args
    proc = Popen(cmd, stdout=DEVNULL, stderr=PIPE)
    out, err = proc.communicate()

    msg = ''
    if err:
        msg = err.decode("utf-8")

    return proc.returncode, msg
