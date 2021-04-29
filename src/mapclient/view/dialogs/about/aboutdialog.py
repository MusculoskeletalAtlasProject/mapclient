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
from PySide2 import QtWidgets

from mapclient.settings import info
from mapclient.view.dialogs.about.ui.ui_aboutdialog import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog):
    """
    About dialog to display program about information.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_AboutDialog()
        self._ui.setupUi(self)
        text = self._ui.aboutTextLabel.text()
        self._ui.aboutTextLabel.setText(text.replace('##version##', info.VERSION_STRING))
        self._makeConnections()

    def _makeConnections(self):
        self._ui.btn_Credits.clicked.connect(self.showCreditsDialog)
        self._ui.btn_License.clicked.connect(self.showLicenseDialog)

    def showCreditsDialog(self):
        from mapclient.view.dialogs.about.creditsdialog import CreditsDialog
        dlg = CreditsDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def showLicenseDialog(self):
        from mapclient.view.dialogs.about.licensedialog import LicenseDialog
        dlg = LicenseDialog(self)
        dlg.setModal(True)
        dlg.exec_()
