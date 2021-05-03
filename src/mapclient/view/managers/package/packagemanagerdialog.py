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
import os

from PySide2 import QtWidgets
from mapclient.view.managers.package.ui.ui_packagemanagerdialog import Ui_PackageManagerDialog


class PackageManagerDialog(QtWidgets.QDialog):
    """
    Dialog for managing the list of plugin directories.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_PackageManagerDialog()
        self._ui.setupUi(self)
        self._ui.removeButton.setEnabled(False)

        self._make_connections()

    def _make_connections(self):
        self._ui.addButton.clicked.connect(self._add_directory_clicked)
        self._ui.directoryListing.itemSelectionChanged.connect(self._directory_selection_changed)
        self._ui.removeButton.clicked.connect(self._remove_button_clicked)

    def _directory_selection_changed(self):
        self._ui.removeButton.setEnabled(len(self._ui.directoryListing.selectedItems()) > 0)

    def _remove_button_clicked(self):
        for item in self._ui.directoryListing.selectedItems():
            self._ui.directoryListing.takeItem(self._ui.directoryListing.row(item))

    def _add_directory_clicked(self):
        selected_items = self._ui.directoryListing.selectedItems()
        last = ''
        if selected_items:
            last_selected_item = selected_items[-1]
            last = last_selected_item
        else:
            last = self._ui.directoryListing.item(self._ui.directoryListing.count() - 1)

        if last:
            last = last.text()

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select Package Directory', dir=last, options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ReadOnly)
        if len(directory) > 0:
            self._ui.directoryListing.addItem(directory)

    def set_directories(self, directories):
        self._ui.directoryListing.addItems([directory for directory in directories if os.path.exists(directory)])

    def directories(self):
        directories = []
        for index in range(self._ui.directoryListing.count()):
            directories.append(self._ui.directoryListing.item(index).text())

        return directories
