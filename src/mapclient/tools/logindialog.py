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
from PySide import QtGui, QtCore

from hashlib import sha224

from mapclient.tools.ui_logindialog import Ui_LoginDialog
from mapclient.tools.registeruser import registerUser

invalid_style_sheet = 'QLabel { background-color: rgba(255, 0, 0, 10); }'

class LoginDialog(QtGui.QDialog):
    '''
    Dialog for identifying user.
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_LoginDialog()
        self._ui.setupUi(self)
        
        self._errorTimer = QtCore.QTimer(self)
        self._errorTimer.setInterval(5000)
        self._errorTimer.setSingleShot(True)
        
        self._makeConnections()
        
        
    def _updateUi(self):
        pass
    
    def _makeConnections(self):
        self._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self._validateLogin)
        self._ui.registerForgotLabel.linkActivated.connect(self._registerOrForgot)
        self._errorTimer.timeout.connect(self._hideErrorMessage)

    def _validateLogin(self):
        username = self._ui.usernameLineEdit.text()
        password = sha224(self._ui.passwordLineEdit.text().encode('utf8')).hexdigest()
        stored_password = 'xxxxxxx'
        
        settings = QtCore.QSettings()
        settings.beginGroup('RegisteredUsers')
        user_exists = username in settings.childGroups()
        if user_exists:
            settings.beginGroup(username)
            stored_password = settings.value('password', '')
            settings.endGroup()
        settings.endGroup()
        
        if user_exists and stored_password == password:
            self.accept()
        else:
            self._loginError()
    
    
    def _registerOrForgot(self, link):
        if link == 'mapclient.register':
            registerUser(self)
            
    def _loginError(self):
        self._ui.errorOutputLabel.setText('Error: login details incorrect')
        self._ui.errorOutputLabel.setStyleSheet(invalid_style_sheet)
        self._errorTimer.start()
        
    def _hideErrorMessage(self):
        self._ui.errorOutputLabel.setText('')
        self._ui.errorOutputLabel.setStyleSheet('')
        
    def username(self):
        return self._ui.usernameLineEdit.text()
    
    
