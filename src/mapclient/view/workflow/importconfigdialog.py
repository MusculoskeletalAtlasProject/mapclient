import os
import shutil

import numpy
import zipfile
import tempfile

from PySide6 import QtCore, QtWidgets
from packaging import version

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, VERSION_STRING
from mapclient.core.utils import load_configuration, copy_step_additional_config_files
from mapclient.core.workflow.workflowitems import MetaStep
from mapclient.view.workflow.workflowgraphicsitems import Node
from mapclient.view.workflow.ui.ui_importconfigdialog import Ui_ImportConfigDialog


class ImportConfigDialog(QtWidgets.QDialog):

    def __init__(self, import_source, graphics_scene, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ImportConfigDialog()
        self._ui.setupUi(self)

        self._import_source = import_source
        self._graphics_scene = graphics_scene
        self._workflow_scene = self._graphics_scene.workflowScene()
        self._undo_stack = self._graphics_scene.getUndoStack()

        self._step_map = None
        self._setup_step_map()
        self._setup_grid_layout()

        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonImport.clicked.connect(self._import_clicked)

    def _import_settings(self):
        if zipfile.is_zipfile(self._import_source):
            # Get project information for the imported workflow.
            with zipfile.ZipFile(self._import_source, mode="r") as archive:
                with tempfile.TemporaryDirectory() as temp_dir:
                    archive.extract(DEFAULT_WORKFLOW_PROJECT_FILENAME, temp_dir)
                    import_proj = QtCore.QSettings(os.path.join(temp_dir, DEFAULT_WORKFLOW_PROJECT_FILENAME), QtCore.QSettings.Format.IniFormat)
        else:
            import_proj = QtCore.QSettings(self._import_source, QtCore.QSettings.Format.IniFormat)

        return import_proj

    @staticmethod
    def _determine_import_steps(import_proj):
        import_proj.beginGroup('nodes')
        node_count = import_proj.beginReadArray('nodelist')
        import_steps = numpy.empty(shape=(node_count,), dtype=[("ID", "<U64"), ("Name", "<U64")])
        for i in range(node_count):
            import_proj.setArrayIndex(i)
            import_steps[i]["ID"] = import_proj.value('identifier')
            import_steps[i]["Name"] = import_proj.value('name')

        return import_steps

    def _determine_workflow_steps(self, node_count):
        # Get workflow information.
        workflow_steps = numpy.empty(shape=(node_count,), dtype=[("ID", "<U64"), ("Name", "<U64")])
        i = 0
        for workflow_item in list(self._workflow_scene.items()):
            if workflow_item.Type == MetaStep.Type:
                workflow_steps[i]["ID"] = workflow_item.getIdentifier()
                workflow_steps[i]["Name"] = workflow_item.getName()
                i += 1

        return workflow_steps

    def _create_step_map(self, node_count, import_steps, workflow_steps):
        # Create a mapping between the current workflow steps and the steps being imported.
        self._step_map = numpy.empty(shape=node_count, dtype=[("ID", "<U64"), ("Name", "<U64"), ("Imports", object), ("Selected", "<U64")])
        self._step_map["ID"] = workflow_steps["ID"]
        self._step_map["Name"] = workflow_steps["Name"]

        # Generate list of choices for each workflow step
        for i in range(len(workflow_steps)):
            self._step_map[i]["Imports"] = ['']
            for j in range(len(import_steps)):
                if workflow_steps[i]["Name"] == import_steps[j]["Name"]:
                    self._step_map[i]["Imports"].append(import_steps[j]["ID"])

        if numpy.array_equal(import_steps["Name"], workflow_steps["Name"]):
            # If the lists of step names match, assign a one-to-one mapping of step indices.
            self._step_map["Selected"] = import_steps["ID"]

    def is_compatible(self):
        import_proj = self._import_settings()
        # Check for version compatibility.
        import_version = version.parse(import_proj.value('version'))
        application_version = version.parse(VERSION_STRING)
        if not _compatible_versions(import_version, application_version):
            QtWidgets.QMessageBox.warning(self, 'Different Workflow Versions', f'The version of the imported workflow ({import_version})'
                                                                               f' is not compatible with this version of the MAP Client ({application_version}).')
            return False

        return True

    def _setup_step_map(self):
        import_proj = self._import_settings()

        node_count = len([_ for _ in self._workflow_scene.items() if (_.Type == MetaStep.Type)])
        import_steps = self._determine_import_steps(import_proj)
        workflow_steps = self._determine_workflow_steps(node_count)

        self._create_step_map(node_count, import_steps, workflow_steps)

    def _update_step_map(self):
        for row_index in range(len(self._step_map)):
            current_text = self._ui.gridLayout.itemAtPosition(row_index + 1, 2).widget().currentText()
            self._step_map[row_index]["Selected"] = current_text

    def _setup_grid_layout(self):
        # Apply the step_map to the GUI.
        grid_layout = self._ui.gridLayout

        for i in range(len(self._step_map)):
            id_line_edit = QtWidgets.QLineEdit(self._step_map[i]["ID"])
            name_line_edit = QtWidgets.QLineEdit(self._step_map[i]["Name"])
            id_line_edit.setEnabled(False)
            name_line_edit.setEnabled(False)
            grid_layout.addWidget(id_line_edit, i + 1, 0)
            grid_layout.addWidget(name_line_edit, i + 1, 1)

            combo_box = QtWidgets.QComboBox()
            combo_box.addItems(self._step_map[i]["Imports"])
            combo_box.setCurrentIndex(self._step_map[i]["Imports"].index(self._step_map[i]["Selected"]))

            grid_layout.addWidget(combo_box, i + 1, 2)

    def _do_import(self, configuration_dir, node_dict):
        self._undo_stack.beginMacro('Import Configurations')
        for row_index in range(len(self._step_map)):
            current_text = self._step_map[row_index]["Selected"]
            if current_text != '':
                identifier = self._step_map[row_index]["ID"]
                node = node_dict[identifier]

                self._graphics_scene.setConfigureNode(node)

                configuration = load_configuration(configuration_dir, current_text)
                meta_step = node.metaItem()
                step = meta_step.getStep()
                current_step_location = step.getLocation()
                step.setLocation(configuration_dir)
                step.deserialize(configuration)
                copy_step_additional_config_files(step, configuration_dir, current_step_location)
                step.setLocation(current_step_location)
                self._workflow_scene.changeIdentifier(meta_step)

                # This method adds the change in configuration to the undo-redo stack.
                self._graphics_scene.stepConfigured()
        self._undo_stack.endMacro()

    def _import_clicked(self):
        self._update_step_map()

        # Import the new configurations into the workflow steps.
        node_dict = {}
        for node in self._graphics_scene.items():
            if hasattr(node, 'Type') and node.Type == Node.Type:
                identifier = node.metaItem().getIdentifier()
                node_dict[identifier] = node

        if zipfile.is_zipfile(self._import_source):
            with zipfile.ZipFile(self._import_source, mode="r") as archive:
                with tempfile.TemporaryDirectory() as temp_dir:
                    archive.extractall(temp_dir)
                    self._do_import(temp_dir, node_dict)
        else:
            self._do_import(os.path.dirname(self._import_source), node_dict)

        QtWidgets.QMessageBox.information(self, "Configurations Imported",
                                          "The selected configurations have been successfully imported.")


def _compatible_versions(import_settings_version, application_version):
    if import_settings_version < version.Version("0.19.0"):
        return False

    significant_import_settings_version = version.Version(f"{import_settings_version.major}.{import_settings_version.minor}")
    if significant_import_settings_version > application_version:
        return False

    return True
