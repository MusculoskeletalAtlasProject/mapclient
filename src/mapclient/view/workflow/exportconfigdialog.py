import os
from zipfile import ZipFile

from PySide6 import QtCore, QtWidgets

from mapclient.core.workflow.workflowitems import MetaStep
from mapclient.settings.general import get_configuration_file
from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME
from mapclient.view.workflow.ui.ui_exportconfigdialog import Ui_ExportConfigDialog


class ExportConfigDialog(QtWidgets.QDialog):

    def __init__(self, workflow_dir, graphics_scene, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ExportConfigDialog()
        self._ui.setupUi(self)

        self._scene = graphics_scene.workflowScene()
        self._default_location = ''
        self._workflow_dir = workflow_dir
        self._setup_list()

        self._update_ui()
        self._make_connections()

    def _make_connections(self):
        self._ui.deselectAllButton.clicked.connect(self._deselect_all)
        self._ui.selectAllButton.clicked.connect(self._select_all)
        self._ui.exportToButton.clicked.connect(self._export_to_button_clicked)
        self._ui.exportButton.clicked.connect(self._export_button_clicked)

    def _setup_list(self):
        for workflow_item in list(self._scene.items()):
            if workflow_item.Type == MetaStep.Type:
                identifier = workflow_item.getStepIdentifier()
                list_item = QtWidgets.QListWidgetItem(identifier)
                list_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self._ui.listWidget.addItem(list_item)

    def _export_button_clicked(self):
        # Gather the workflow project files.
        archive_files = []
        for filename in [DEFAULT_WORKFLOW_PROJECT_FILENAME, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME]:
            project_file = os.path.join(self._workflow_dir, filename)
            if os.path.isfile(project_file):
                archive_files.append(project_file)

        # Check the workflow-steps for config files.
        wanted_configurations = self._get_selected_items()
        for workflow_item in list(self._scene.items()):
            if workflow_item.Type == MetaStep.Type:
                identifier = workflow_item.getIdentifier()
                if identifier in wanted_configurations:
                    archive_files.append(get_configuration_file(self._workflow_dir, identifier))
                    additional_config_files = workflow_item.getStep().getAdditionalConfigFiles()
                    archive_files.extend([os.path.relpath(config_file, self._workflow_dir) for config_file in additional_config_files])

        # Zip files and store in export destination.
        export_zip = self._ui.exportToLineEdit.text()
        if export_zip:
            with ZipFile(export_zip, mode="w") as archive:
                for archive_file in archive_files:
                    archive.write(archive_file, arcname=os.path.relpath(archive_file, self._workflow_dir))

        self.accept()

    def _export_to_button_clicked(self):
        export_zip, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Select Export File', dir=self._default_location,
                                                              filter='Data files(*.zip)')
        self._ui.exportToLineEdit.setText(export_zip)
        self._update_ui()

    def _update_ui(self):
        self._ui.exportButton.setEnabled(len(self._ui.exportToLineEdit.text()) > 0)

    def _select_all(self):
        for i in range(self._ui.listWidget.count()):
            self._ui.listWidget.item(i).setCheckState(QtCore.Qt.CheckState.Checked)

    def _deselect_all(self):
        for i in range(self._ui.listWidget.count()):
            self._ui.listWidget.item(i).setCheckState(QtCore.Qt.CheckState.Unchecked)

    def _get_selected_items(self):
        return [
            self._ui.listWidget.item(i).text()
            for i in range(self._ui.listWidget.count())
            if self._ui.listWidget.item(i).checkState() == QtCore.Qt.CheckState.Checked
        ]

    def setDefaultLocation(self, default_location):
        self._default_location = default_location
