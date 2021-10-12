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
import json

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QFileDialog

from mapclientplugins.pointcloudserializerstep.widgets.ui_configuredialog import Ui_ConfigureDialog

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'


class ConfigureDialogState(object):
    """
    Class to encapsulate the state of the configure dialog so that the 
    dialog state can be persistent.
    """

    def __init__(self, output_directory='', default_directory=True):
        self._output_directory = output_directory
        self._default_directory = default_directory
        
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

        self._workflow_location = None

        self._previous_location = ''

        self.setState(state)
        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEditOutputLocation.textChanged.connect(self.extended_validate)
        self._ui.checkBoxDefaultLocation.clicked.connect(self.validate)
        self._ui.pushButtonOutputLocation.clicked.connect(self._output_location_button_clicked)

    def _output_location_button_clicked(self):
        location, _ = QFileDialog.getSaveFileName(self, caption='Choose Output File', dir=self._previous_location)
        if location:
            self._previous_location = location

            if self._workflow_location:
                self._ui.lineEditOutputLocation.setText(os.path.relpath(location, self._workflow_location))
            else:
                self._ui.lineEditOutputLocation.setText(location)

    def setState(self, state):
        self._ui.lineEditOutputLocation.setText(state._output_directory)
        self._ui.checkBoxDefaultLocation.setChecked(state._default_directory)

    def getState(self):
        state = ConfigureDialogState(
            self._ui.lineEditOutputLocation.text(),
            self._ui.checkBoxDefaultLocation.isChecked()
        )

        return state

    def set_workflow_location(self, location):
        self._workflow_location = location

    def validate(self):
        output_path = self._ui.lineEditOutputLocation.text()
        output_directory = os.path.dirname(output_path)
        non_empty = len(output_path)

        if not os.path.isabs(output_path):
            output_path = os.path.join(self._workflow_location, output_path)
            output_directory = os.path.join(self._workflow_location, output_directory)

        output_directory_valid = os.path.exists(output_directory) and non_empty
        default_directory_checked = self._ui.checkBoxDefaultLocation.isChecked()

        if output_directory_valid:
            self._ui.lineEditOutputLocation.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEditOutputLocation.setStyleSheet(REQUIRED_STYLE_SHEET)
            self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self._ui.checkBoxDefaultLocation.isChecked())

        return output_directory_valid or default_directory_checked

    def extended_validate(self):
        valid = self.validate()

        output_path = self._ui.lineEditOutputLocation.text()
        output_directory_valid = os.path.exists(os.path.dirname(output_path)) and len(output_path)

        if output_directory_valid:
            self._ui.checkBoxDefaultLocation.setChecked(False)

        return valid
