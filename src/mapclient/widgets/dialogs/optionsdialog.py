'''
Created on Feb 25, 2015

@author: hsorby
'''
from PySide import QtGui

from mapclient.widgets.dialogs.ui_optionsdialog import Ui_OptionsDialog

class  OptionsDialog(QtGui.QDialog):
    '''
    Options dialog for setting global options
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)
        self._original_options = {}

    def load(self, options):
        self._original_options = options
        option_name = self._ui.checkBoxShowStepNames.objectName()
        if option_name in options:
            self._ui.checkBoxShowStepNames.setChecked(options[option_name])

    def save(self):
        options = {}
        options[self._ui.checkBoxShowStepNames.objectName()] = self._ui.checkBoxShowStepNames.isChecked()

        return options

    def isModified(self):
        return not self._original_options == self.save()

