'''
Created on Jun 10, 2015

@author: hsorby
'''
from mapclient.core.utils import which
from mapclient.settings.general import getVirtEnvDirectory
from mapclient.core.checks import getPySideRccExecutable, getPySideUicExecutable
from mapclient.settings.definitions import SHOW_STEP_NAMES, \
    DONT_CREATE_VIRTUAL_ENV, OPTIONS_SETTINGS_TAG, PYSIDE_UIC_EXE, \
    PYSIDE_RCC_EXE, VIRTUAL_ENV_PATH, GIT_EXE

class OptionsManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._options = {}
        # Set default values
        self._options[SHOW_STEP_NAMES] = True
        self._options[DONT_CREATE_VIRTUAL_ENV] = False
        self._options[PYSIDE_UIC_EXE] = getPySideUicExecutable()
        self._options[PYSIDE_RCC_EXE] = getPySideRccExecutable()
        self._options[VIRTUAL_ENV_PATH] = getVirtEnvDirectory()
        self._options[GIT_EXE] = which('git')


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
            if option == SHOW_STEP_NAMES:
                self._options[option] = settings.value(option) == 'true'
            elif option == DONT_CREATE_VIRTUAL_ENV:
                self._options[option] = settings.value(option) == 'true'
            else:
                self._options[option] = settings.value(option)
        settings.endGroup()


