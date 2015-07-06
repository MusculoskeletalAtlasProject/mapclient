'''
Created on Jun 10, 2015

@author: hsorby
'''

class OptionsManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._options = {}

    def getOptions(self):
        return self._options

    def setOptions(self, options):
        self._options = options

    def writeSettings(self, settings):
        settings.beginGroup('Options')
        for option in self._options:
            settings.setValue(option, self._options[option])
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup('Options')
        options = settings.allKeys()
        for option in options:
            if option == 'checkBoxShowStepNames':
                self._options[option] = settings.value(option) == 'true'
            else:
                self._options[option] = settings.value(option)
        settings.endGroup()


