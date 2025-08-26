"""
Created on Jun 10, 2015

@author: hsorby
"""
from mapclient.core.utils import which
from mapclient.settings.general import get_virtualenv_directory
from mapclient.settings.definitions import SHOW_STEP_NAMES, CLOSE_AFTER, METRICS_PERMISSION, INTERNAL_EXE, UNSET_FLAG, \
    DONT_CREATE_VIRTUAL_ENV, OPTIONS_SETTINGS_TAG, INTERNAL_WORKFLOWS_AVAILABLE, INTERNAL_WORKFLOW_DIR, VIRTUAL_ENV_PATH, \
    GIT_EXE, PYSIDE_UIC_EXE, PYSIDE_RCC_EXE, PREVIOUS_PW_WRITE_STEP_LOCATION, PREVIOUS_PW_ICON_LOCATION, \
    CHECK_TOOLS_ON_STARTUP, \
    USE_EXTERNAL_GIT, USE_EXTERNAL_RCC, USE_EXTERNAL_UIC, RECENTS_ABSOLUTE_PATHS, RECENTS_LENGTH, PREVIOUS_WORKFLOW, \
    AUTOLOAD_PREVIOUS_WORKFLOW, METRICS_PERMISSION_ATTAINED, ANIMATE_LAYOUT_UPDATES


def _is_boolean(option):
    return option in [SHOW_STEP_NAMES, CHECK_TOOLS_ON_STARTUP, DONT_CREATE_VIRTUAL_ENV, METRICS_PERMISSION, USE_EXTERNAL_GIT,
                      USE_EXTERNAL_RCC, USE_EXTERNAL_UIC, RECENTS_ABSOLUTE_PATHS, INTERNAL_WORKFLOWS_AVAILABLE,
                      AUTOLOAD_PREVIOUS_WORKFLOW, ANIMATE_LAYOUT_UPDATES]


def _is_float(option):
    return option in [CLOSE_AFTER]


def _is_int(option):
    return option in [RECENTS_LENGTH]


class OptionsManager(object):

    def __init__(self):
        # Set default values
        self._options = {
            SHOW_STEP_NAMES: True, CLOSE_AFTER: 2.0, METRICS_PERMISSION: False,
            DONT_CREATE_VIRTUAL_ENV: False, CHECK_TOOLS_ON_STARTUP: True,
            ANIMATE_LAYOUT_UPDATES: True,
            USE_EXTERNAL_GIT: False, USE_EXTERNAL_RCC: False, USE_EXTERNAL_UIC: False,
            RECENTS_ABSOLUTE_PATHS: False, RECENTS_LENGTH: 10,
            VIRTUAL_ENV_PATH: get_virtualenv_directory(), GIT_EXE: which('git'),
            PYSIDE_RCC_EXE: INTERNAL_EXE, PYSIDE_UIC_EXE: INTERNAL_EXE,
            PREVIOUS_PW_WRITE_STEP_LOCATION: '', PREVIOUS_PW_ICON_LOCATION: '',
            INTERNAL_WORKFLOWS_AVAILABLE: False, INTERNAL_WORKFLOW_DIR: UNSET_FLAG,
            PREVIOUS_WORKFLOW: UNSET_FLAG, AUTOLOAD_PREVIOUS_WORKFLOW: True,
            METRICS_PERMISSION_ATTAINED: {}
        }

    def getOptions(self):
        return self._options

    def getOption(self, option):
        if option in self._options:
            return self._options[option]

        return None

    def setOptions(self, options):
        self._options = options

    def setOption(self, option, value):
        self._options[option] = value

    def writeSettings(self, settings):
        settings.beginGroup(OPTIONS_SETTINGS_TAG)
        for option in self._options:
            settings.setValue(option, self._options[option])
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(OPTIONS_SETTINGS_TAG)
        options = settings.allKeys()
        for option in options:
            if _is_boolean(option):
                self._options[option] = settings.value(option) == 'true'
            elif _is_float(option):
                self._options[option] = float(settings.value(option))
            elif _is_int(option):
                self._options[option] = int(settings.value(option))
            else:
                self._options[option] = settings.value(option)
        settings.endGroup()
