"""
This tool is used to update out of date MAP Client workflows.
"""

import os

from packaging import version

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME
from mapclient.tools.updateworkflow.ui.ui_updateworkflowdialog import Ui_UpdateWorkflowDialog


class UpdateWorkflowDialog(QDialog):
    """
    Manages version information for MAP Client workflows.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_UpdateWorkflowDialog()
        self._ui.setupUi(self)

        self._selected_workflow_version = None
        self._workflow_location = None

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
        elif version.parse(self._selected_workflow_version) < version.parse("0.16.0"):
            self._update_to_version_0_16_0(".workflow.conf")
            QMessageBox.information(self, 'Update Confirmed', 'Workflow updated to version 0.16.0\t')
        elif version.parse(self._selected_workflow_version) == version.parse("0.16.0") and os.path.exists(os.path.join(self._workflow_location, "workflow.conf")):
            self._update_to_version_0_16_0("workflow.conf")
            QMessageBox.information(self, 'Update Confirmed', 'Workflow patched to version 0.16.0\t')
        else:
            QMessageBox.information(self, 'Update', 'The selected workflow is already up to date\t')

    def _update_to_version_0_16_0(self, workflow_conf_file):
        current_workflow_conf_location = os.path.join(self._workflow_location, workflow_conf_file)
        new_workflow_conf_location = os.path.join(self._workflow_location, DEFAULT_WORKFLOW_PROJECT_FILENAME)
        os.rename(current_workflow_conf_location, new_workflow_conf_location)

        current_workflow_rdf_location = os.path.join(self._workflow_location, ".workflow.rdf")
        new_workflow_rdf_location = os.path.join(self._workflow_location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME)
        os.rename(current_workflow_rdf_location, new_workflow_rdf_location)

        current_workflow_req_location = os.path.join(self._workflow_location, ".workflow.req")
        if os.path.exists(current_workflow_req_location):
            new_workflow_req_location = os.path.join(self._workflow_location, DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME)
            os.rename(current_workflow_req_location, new_workflow_req_location)

        workflow_conf = QSettings(new_workflow_conf_location, QSettings.IniFormat)
        workflow_conf.setValue('version', '0.16.0')

    def _choose_workflow_clicked(self):
        """
        Select the workflow directory given by the user.
        """
        location = QFileDialog.getExistingDirectory(self, 'Select Directory', self._workflow_location)

        if location:
            self._workflow_location = location

            self._selected_workflow_version = _get_workflow_version(location)
            if self._selected_workflow_version is not None:
                self._ui.lineEditStepLocation.setText(location)
            else:
                QMessageBox.warning(self, 'Update',
                                    'Target directory is not recognized as a MAP Client workflow directory')


def _get_workflow_version(location):
    """
    Attempt to read a workflow version from the given directory. If a version identifier is found return the
    version, otherwise return None.
    """
    if os.path.isfile(os.path.join(location, ".workflow.conf")):
        target_file = os.path.join(location, ".workflow.conf")
    elif os.path.isfile(os.path.join(location, "workflow.conf")):
        target_file = os.path.join(location, "workflow.conf")
    elif os.path.isfile(os.path.join(location, DEFAULT_WORKFLOW_PROJECT_FILENAME)):
        target_file = os.path.join(location, DEFAULT_WORKFLOW_PROJECT_FILENAME)
    else:
        return None

    workflow_conf = QSettings(target_file, QSettings.IniFormat)
    workflow_version = workflow_conf.value('version')

    return workflow_version
