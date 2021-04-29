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
from PySide2 import QtWidgets

from mapclient.tools.pmr.ui_oauthcheckdialog import Ui_OAuthCheckDialog

logger = logging.getLogger(__name__)


class OAuthCheckDialog(QtWidgets.QDialog):
    """
    Dialog that other UI elements can spawn to check for existence of
    token credentials and acquire one from user if it is unavailable.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_OAuthCheckDialog()
        self._ui.setupUi(self)
        self._makeConnections()

    def _makeConnections(self):
        self._ui.continueButton.clicked.connect(self.event_register)

    def token(self):
        return self._ui.tokenLineEdit.text()

