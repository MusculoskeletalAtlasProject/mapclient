"""
This tool is used to update out of date MAP Client workflows.
"""

import os

from packaging import version

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

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
        self._ui.pushButtonUpdate.setEnabled(False)

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
        title = 'Update'
        messages = []
        if version.parse(self._selected_workflow_version) < version.parse("0.16.0"):
            _update_to_version_0_16_0(self._workflow_location, ".workflow.conf")
            title = 'Update Confirmed'
            messages.append('Workflow updated to version 0.16.0\t')
        elif version.parse(self._selected_workflow_version) == version.parse("0.16.0") and os.path.exists(os.path.join(self._workflow_location, "workflow.conf")):
            _update_to_version_0_16_0(self._workflow_location, "workflow.conf")
            title = 'Update Confirmed'
            messages.append('Workflow patched to version 0.16.0\t')

        if _update_scaffold_creator_rename(self._workflow_location):
            title = 'Update Confirmed'
            messages.append('Renamed Mesh Generator to Scaffold Creator\t')

        if _update_geometry_fitter_rename(self._workflow_location):
            title = 'Update Confirmed'
            messages.append('Renamed Geometric Fit to Geometry Fitter\t')

        self._show_message(title, messages)

    def _show_message(self, title, messages):
        if len(messages):
            text = '\n'.join(messages)
        else:
            text = 'The selected workflow is already up to date\t'
        QMessageBox.information(self, title, text)

    def _choose_workflow_clicked(self):
        """
        Select the workflow directory given by the user.
        """
        location = QFileDialog.getExistingDirectory(self, 'Select Directory', self._workflow_location)

        if location:
            self._workflow_location = location

            self._selected_workflow_version = _get_workflow_version(location)
            if self._selected_workflow_version is not None:
                self._ui.pushButtonUpdate.setEnabled(True)
                self._ui.lineEditStepLocation.setText(location)
            else:
                self._ui.pushButtonUpdate.setEnabled(False)
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


def _update_to_version_0_16_0(workflow_location, workflow_conf_file):
    current_workflow_conf_location = os.path.join(workflow_location, workflow_conf_file)
    new_workflow_conf_location = os.path.join(workflow_location, DEFAULT_WORKFLOW_PROJECT_FILENAME)
    os.rename(current_workflow_conf_location, new_workflow_conf_location)

    current_workflow_rdf_location = os.path.join(workflow_location, ".workflow.rdf")
    new_workflow_rdf_location = os.path.join(workflow_location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME)
    os.rename(current_workflow_rdf_location, new_workflow_rdf_location)

    current_workflow_req_location = os.path.join(workflow_location, ".workflow.req")
    if os.path.exists(current_workflow_req_location):
        new_workflow_req_location = os.path.join(workflow_location, DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME)
        os.rename(current_workflow_req_location, new_workflow_req_location)

    workflow_conf = QSettings(new_workflow_conf_location, QSettings.IniFormat)
    workflow_conf.setValue('version', '0.16.0')


def _rename_step(workflow_location, old_name, new_name, new_src_uri):
    updated = False
    workflow_conf_location = os.path.join(workflow_location, DEFAULT_WORKFLOW_PROJECT_FILENAME)
    workflow_conf = QSettings(workflow_conf_location, QSettings.IniFormat)

    workflow_conf.beginGroup('nodes')
    node_count = workflow_conf.beginReadArray('nodelist')

    name_indices = []
    for i in range(node_count):
        workflow_conf.setArrayIndex(i)
        name = workflow_conf.value('name')
        if name == old_name:
            name_indices.append(i)

    workflow_conf.endArray()
    workflow_conf.beginWriteArray('nodelist')

    for i in range(node_count):
        workflow_conf.setArrayIndex(i)
        if i in name_indices:
            workflow_conf.setValue('name', new_name)
            workflow_conf.setValue('source_uri', new_src_uri)
            updated = True

    workflow_conf.endArray()
    workflow_conf.endGroup()

    return updated


def _update_scaffold_creator_rename(workflow_location):
    new_name = "Scaffold Creator"
    new_src_uri = "https://github.com/ABI-Software/mapclientplugins.scafffoldcreator"

    return _rename_step(workflow_location, "Mesh Generator", new_name, new_src_uri)


def _update_geometry_fitter_rename(workflow_location):
    new_name = "Geometry Fitter"
    new_src_uri = "https://github.com/ABI-Software/mapclientplugins.geometryfitter"

    return _rename_step(workflow_location, "Geometric Fit", new_name, new_src_uri)
