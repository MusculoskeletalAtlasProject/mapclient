
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

from PySide2.QtWidgets import QDialog, QFileDialog, QDialogButtonBox

from mapclientplugins.imagesourcestep.widgets.ui_configuredialog import Ui_ConfigureDialog
from mapclient.tools.pmr.pmrworkflowwidget import PMRWorkflowWidget
import os
from mapclient.tools.pmr.pmrtool import ontological_search_string, \
    plain_text_search_string

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'


class ConfigureDialogState(object):

    def __init__(self, local_location='', pmr_location='', image_type=0, current_tab=0, previous_local_location=''):
        self._local_location = local_location
        self._pmr_location = pmr_location
        self._image_type = image_type
        self._current_tab = current_tab
        self._previous_local_location = previous_local_location

    def location(self):
        return self._local_location

    def setLocation(self, location):
        self._local_location = location

    def pmrLocation(self):
        return self._pmr_location

    def imageType(self):
        return self._image_type

    def currentTab(self):
        return self._current_tab

    def previousLocalLocation(self):
        return self._previous_local_location

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
        self._setupPMRTab()
        self._workflow_location = None

        self.setState(state)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.localLineEdit.textChanged.connect(self._localLocationEdited)
        self._ui.localButton.clicked.connect(self._localLocationClicked)
        # self._pmr_widget._ui.lineEditWorkspace.textChanged.connect(self._workspaceChanged)
        # self._ui.pmrRegisterLabel.linkActivated.connect(self._register)

    def _setupPMRTab(self):
        self._pmr_widget = PMRWorkflowWidget(self)
        self._pmr_widget.setImport(False)
        self._pmr_widget.setExport(False)
        self._pmr_widget.setSearchDomain([ontological_search_string, plain_text_search_string])

        layout = self._ui.pmrTab.layout()
        layout.addWidget(self._pmr_widget)

    def setState(self, state):
        self._ui.localLineEdit.setText(state.location())
        self._pmr_widget.setWorkspaceUrl(state.pmrLocation())
        self._ui.imageSourceTypeComboBox.setCurrentIndex(state.imageType())
        self._ui.tabWidget.setCurrentIndex(state.currentTab())
        self._ui.previousLocationLabel.setText(state.previousLocalLocation())

    def getState(self):
        state = ConfigureDialogState(
            self._ui.localLineEdit.text(),
            self._pmr_widget.workspaceUrl(),
            self._ui.imageSourceTypeComboBox.currentIndex(),
            self._ui.tabWidget.currentIndex(),
            self._ui.previousLocationLabel.text())

        return state

    def _localLocationClicked(self):
        location = QFileDialog.getExistingDirectory(self, 'Select Image File(s) Location', self._ui.previousLocationLabel.text())

        if location:
            self._ui.previousLocationLabel.setText(location)

            if self._workflow_location:
                self._ui.localLineEdit.setText(os.path.relpath(location, self._workflow_location))
            else:
                self._ui.localLineEdit.setText(location)

    def _workspaceChanged(self, text):
        pass

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def _localLocationEdited(self):
        self.validate()

    def localLocation(self):
        return self._ui.localLineEdit.text()

    def validate(self):
        directory = self._ui.localLineEdit.text()
        non_empty = len(directory)

        if not os.path.isabs(directory):
            directory = os.path.join(self._workflow_location, directory)

        directory_valid = os.path.exists(directory)

        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(directory_valid)
        self._ui.localLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else REQUIRED_STYLE_SHEET)

        return directory_valid


