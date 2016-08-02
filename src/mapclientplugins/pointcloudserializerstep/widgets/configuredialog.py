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
import json

from PySide.QtGui import QDialog, QDialogButtonBox

from mapclientplugins.pointcloudserializerstep.widgets.ui_configuredialog import Ui_ConfigureDialog

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'

class ConfigureDialogState(object):
    """
    Class to encapsulate the state of the configure dialog so that the 
    dialog state can be persistent.
    """


    def __init__(self, identifier=''):
        self._identifier = identifier

    def identifier(self):
        return self._identifier

    def setIdentifier(self, identifier):
        self._identifier = identifier
        
    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def deserialize(self, string):
        self.__dict__.update(json.loads(string))


class ConfigureDialog(QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, state, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
        self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        self.setState(state)
        self.validate()
        self._makeConnections()

    def _makeConnections(self):
        self._ui.identifierLineEdit.textChanged.connect(self.validate)

    def setState(self, state):
        self._ui.identifierLineEdit.setText(state._identifier)

    def getState(self):
        state = ConfigureDialogState(
            self._ui.identifierLineEdit.text())

        return state

    def validate(self):
        identifierValid = len(self._ui.identifierLineEdit.text()) > 0

        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(identifierValid)

        if identifierValid:
            self._ui.identifierLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        return identifierValid

