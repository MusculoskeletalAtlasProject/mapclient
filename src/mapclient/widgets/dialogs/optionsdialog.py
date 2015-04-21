'''
Created on Feb 25, 2015

@author: hsorby
'''
from PySide import QtGui

from mapclient.widgets.dialogs.ui_optionsdialog import Ui_OptionsDialog

class OptionsDialog(QtGui.QDialog):
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
        
    def load(self, options):
        pass
    
    def save(self):
        options = {}
        return options