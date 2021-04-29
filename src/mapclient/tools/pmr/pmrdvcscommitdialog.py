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
from PySide2 import QtGui, QtWidgets

from mapclient.tools.pmr.ui_pmrdvcscommitdialog import Ui_PMRDVCSCommitDialog


class PMRDVCSCommitDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_PMRDVCSCommitDialog()
        self._ui.setupUi(self)

        self._activated_action = QtWidgets.QDialogButtonBox.Cancel

        tick_icon = QtGui.QIcon(':/pmr/images/tick_yellow.png')
        skip_commit_button = self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        skip_commit_button.setText('Skip Commit')
        skip_commit_button.setIcon(tick_icon)
        skip_commit_button.clicked.connect(self._handleCommit)

        tick_icon = QtGui.QIcon(':/pmr/images/tick_blue.png')
        commit_local_button = self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        commit_local_button.setText('Commit Local')
        commit_local_button.setIcon(tick_icon)
        commit_local_button.clicked.connect(self._handleCommit)

        tick_icon = QtGui.QIcon(':/pmr/images/tick_green.png')
        commit_pmr_button = self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.SaveAll)
        commit_pmr_button.setText('Commit PMR')
        commit_pmr_button.setIcon(tick_icon)
        commit_pmr_button.clicked.connect(self._handleCommit)

    def _handleCommit(self):
        if len(self._ui.commentTextEdit.toPlainText()):
            sender = self.sender()
            if sender == self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok):
                self._activated_action = QtWidgets.QDialogButtonBox.Ok
            elif sender == self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save):
                self._activated_action = QtWidgets.QDialogButtonBox.Save
            elif sender == self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.SaveAll):
                self._activated_action = QtWidgets.QDialogButtonBox.SaveAll
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, 'Error', 'Commit requires a comment')

    def comment(self):
        return self._ui.commentTextEdit.toPlainText()

    def action(self):
        return self._activated_action

