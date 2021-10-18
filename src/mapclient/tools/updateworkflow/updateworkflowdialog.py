"""
This tool is used to update out of date MAP Client workflows.
"""

import os

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox

from mapclient.settings import info
from mapclient.tools.updateworkflow.ui.ui_updateworkflowdialog import Ui_UpdateWorkflowDialog


class UpdateWorkflowDialog(QDialog):
    """
    Manages version information for MAP Client workflows.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_UpdateWorkflowDialog()
        self._ui.setupUi(self)

        self._application_version = version_tuple(info.VERSION_STRING)
        self._selected_workflow_version = None
        self._previous_location = None

        self._make_connections()


    def _make_connections(self):
        self._ui.pushButtonUpdate.clicked.connect(self._update_clicked)
        self._ui.pushButtonStepChooser.clicked.connect(self._choose_workflow_clicked)


    def _update_clicked(self):
        """
        Update the selected workflow to the MAP Client version.
        """
        if self._selected_workflow_version is None:
            QMessageBox.warning(self, 'Update', 'Please select a valid workflow directory')

        # Is there a better approach than nested if blocks (if less than version 16, check if less than version 15, etc)?
        elif self._selected_workflow_version[1] < 16:
            current_workflow_conf_location = os.path.join(self._previous_location, ".workflow.conf")
            new_workflow_conf_location = os.path.join(self._previous_location, "workflow.conf")
            os.rename(current_workflow_conf_location, new_workflow_conf_location)

            workflow_conf = QSettings(new_workflow_conf_location, QSettings.IniFormat)
            workflow_conf.setValue('version', '0.16.0')

            QMessageBox.information(self, 'Update Confirmed', 'Workflow updated to version 0.16.0\t')

        else:
            QMessageBox.information(self, 'Update', 'The selected workflow is already up to date\t')


    def _choose_workflow_clicked(self):
        """
        Select the workflow directory given by the user.
        """
        location = QFileDialog.getExistingDirectory(self, 'Select Directory', self._previous_location)

        if location:
            self._previous_location = location

            self._selected_workflow_version = self._get_workflow_version(location)
            if self._selected_workflow_version is not None:
                self._ui.lineEditStepLocation.setText(location)
            else:
                QMessageBox.warning(self, 'Update',
                                          'Target directory is not recognized as a MAP Client workflow directory')


    def _get_workflow_version(self, location):
        """
        Attempt to read a workflow version from the given directory. If a version identifier is found return the
        version, otherwise return None.
        """
        if (os.path.isfile(os.path.join(location, ".workflow.conf"))):
            target_file = os.path.join(location, ".workflow.conf")
        elif (os.path.isfile(os.path.join(location, "workflow.conf"))):
            target_file = os.path.join(location, "workflow.conf")
        else:
            return None

        workflow_conf = QSettings(target_file, QSettings.IniFormat)
        workflow_version = version_tuple(workflow_conf.value('version'))

        return workflow_version


def version_tuple(version):
    return tuple(map(int, (version.split("."))))