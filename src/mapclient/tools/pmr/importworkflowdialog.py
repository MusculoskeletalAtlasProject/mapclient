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
import os.path

from PySide6 import QtWidgets, QtCore

from mapclient.tools.pmr.ui.ui_importworkflowdialog import Ui_ImportWorkflowDialog
from mapclient.tools.pmr.pmrworkflowwidget import PMRWorkflowWidget
from mapclient.tools.pmr.pmrtool import workflow_search_string


class ImportWorkflowDialog(QtWidgets.QDialog):

    def __init__(self, previous_location, use_external_git, parent=None):
        super(ImportWorkflowDialog, self).__init__(parent)
        self._ui = Ui_ImportWorkflowDialog()
        self._ui.setupUi(self)

        self._previousLocation = previous_location
        self._use_external_git = use_external_git

        self._setupPMRWidget()
        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEditLocation.returnPressed.connect(self._setDestination)
        self._ui.pushButtonLocation.clicked.connect(self._setDestination)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            return True
        return QtWidgets.QDialog.keyPressEvent(self, event)

    def _setupPMRWidget(self):
        self._pmr_widget = PMRWorkflowWidget(self._use_external_git, self)
        self._pmr_widget.setExport(False)
        self._pmr_widget.setImport(False)
        self._pmr_widget.setSearchDomain(workflow_search_string)
        self._pmr_widget._ui.lineEditSearch.setFocus()
        self._pmr_widget._ui.lineEditSearch.returnPressed.connect(self._pmr_widget._searchClicked)
        layout = self.layout()
        # Save a little time by setting the layout disabled while
        # the layout is being de-constructed and constructed again.
        layout.setEnabled(False)
        # Remove the existing items in the layout
        existing_items = []
        for index in range(layout.count(), 0, -1):
            existing_items.append(layout.takeAt(index - 1))

        # Put all the items into the layout in the desired order
        layout.addWidget(self._pmr_widget)
        existing_items.reverse()
        for item in existing_items:
            layout.addItem(item)
        layout.setEnabled(True)

    def destinationDir(self):
        return self._ui.lineEditLocation.text()

    def workspaceUrl(self):
        return self._pmr_widget.workspaceUrl()

    def accept(self, *args, **kwargs):
        destination_dir = self.destinationDir()
        workspace_url = self.workspaceUrl()
        if os.path.exists(destination_dir) and workspace_url:
            return QtWidgets.QDialog.accept(self, *args, **kwargs)
        else:
            QtWidgets.QMessageBox.critical(self, 'Error Caught', "Invalid Import Settings.  Either the workspace url '%s' was not set" \
                                       " or the destination directory '%s' does not exist. " % (workspace_url, destination_dir))

    def _setDestination(self):
        workflowDir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select Workflow Directory', dir=self._previousLocation)
        if workflowDir:
            self._ui.lineEditLocation.setText(workflowDir)


