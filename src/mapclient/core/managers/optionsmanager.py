"""
Created on Jun 10, 2015

@author: hsorby
"""
from mapclient.core.utils import which
from mapclient.settings.general import get_virtualenv_directory
from mapclient.core.checks import get_pyside_rcc_executable
from mapclient.settings.definitions import SHOW_STEP_NAMES, \
    DONT_CREATE_VIRTUAL_ENV, OPTIONS_SETTINGS_TAG, \
    PYSIDE_RCC_EXE, VIRTUAL_ENV_PATH, GIT_EXE, PREVIOUS_PW_WRITE_STEP_LOCATION, \
    PREVIOUS_PW_ICON_LOCATION, CHECK_TOOLS_ON_STARTUP, USE_EXTERNAL_GIT


class OptionsManager(object):

    def __init__(self):
        self._options = {SHOW_STEP_NAMES: True, DONT_CREATE_VIRTUAL_ENV: False, CHECK_TOOLS_ON_STARTUP: True,
                         USE_EXTERNAL_GIT: False, PYSIDE_RCC_EXE: get_pyside_rcc_executable(),
                         VIRTUAL_ENV_PATH: get_virtualenv_directory(), GIT_EXE: which('git'),
                         PREVIOUS_PW_WRITE_STEP_LOCATION: '', PREVIOUS_PW_ICON_LOCATION: ''}
        # Set default values

    def _isBoolean(self, option):
        return option in [SHOW_STEP_NAMES, CHECK_TOOLS_ON_STARTUP, DONT_CREATE_VIRTUAL_ENV, USE_EXTERNAL_GIT]

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
            if self._isBoolean(option):
                self._options[option] = settings.value(option) == 'true'
            else:
                self._options[option] = settings.value(option)
        settings.endGroup()


