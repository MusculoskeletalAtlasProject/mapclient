'''
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
'''
from hashlib import sha224

from PySide import QtGui, QtCore

from mapclient.tools.ui_registerdialog import Ui_RegisterDialog

invalid_style_sheet = 'QLineEdit { background-color: rgba(255, 0, 0, 10); }'

class RegisterDialog(QtGui.QDialog):
    '''
    Dialog for registering a user.
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_RegisterDialog()
        self._ui.setupUi(self)
        
        self._autoUpdateEmailText = True
        self._makeConnections()
        self._updateUi()
        
    def _updateUi(self):
        
        username = self._ui.usernameLineEdit.text()
        
        settings = QtCore.QSettings()
        settings.beginGroup('RegisteredUsers')
        user_exists = username in settings.childGroups()
        settings.endGroup()
        
        valid_username = not (user_exists or len(username) == 0)
        if not valid_username:
            self._ui.usernameLineEdit.setStyleSheet(invalid_style_sheet)
        else:
            self._ui.usernameLineEdit.setStyleSheet('')
        
        valid_password = self._isPasswordValid()
        if not valid_password:
            self._ui.passwordLineEdit.setStyleSheet(invalid_style_sheet)
            self._ui.confirmPasswordLineEdit.setStyleSheet(invalid_style_sheet)
        else:
            self._ui.passwordLineEdit.setStyleSheet('')
            self._ui.confirmPasswordLineEdit.setStyleSheet('')

        disable = True
        if valid_username and valid_password and \
           len(self._ui.emailLineEdit.text()) > 0:
            disable = False
            
        self._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(disable)
        
    def _makeConnections(self):
        self._ui.usernameLineEdit.textEdited.connect(self._updateUi)
        self._ui.usernameLineEdit.textEdited.connect(self._updateEmail)
        self._ui.emailLineEdit.editingFinished.connect(self._updateUi)
        self._ui.emailLineEdit.textEdited.connect(self._stopUpdateEmail)
        self._ui.passwordLineEdit.editingFinished.connect(self._updateUi)
        self._ui.confirmPasswordLineEdit.textEdited.connect(self._updateUi)
        
    def username(self):
        return self._ui.usernameLineEdit.text()
    
    def email(self):
        return self._ui.emailLineEdit.text()
    
    def password(self):
        return sha224(self._ui.passwordLineEdit.text().encode('utf8')).hexdigest()
    
    def _updateEmail(self, new_text):
        if self._autoUpdateEmailText:
            self._ui.emailLineEdit.setText(new_text + '@')
    
    def _stopUpdateEmail(self):
        self._autoUpdateEmailText = False
        
    def _isPasswordValid(self):
        if len(self._ui.passwordLineEdit.text()) == 0:
            return False
        
        p1 = sha224(self._ui.passwordLineEdit.text().encode('utf8')).hexdigest()
        pc = sha224(self._ui.confirmPasswordLineEdit.text().encode('utf8')).hexdigest()
        
        return p1 == pc
    
    
    
