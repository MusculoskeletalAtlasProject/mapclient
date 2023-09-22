import os
import numpy
import zipfile
import tempfile

from PySide6 import QtCore, QtWidgets

from mapclient.settings import version as app_version
from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME
from mapclient.core.utils import loadConfiguration
from mapclient.core.workflow.workflowitems import MetaStep
from mapclient.view.workflow.workflowgraphicsitems import Node
from mapclient.view.workflow.ui.ui_importconfigdialog import Ui_ImportConfigDialog


class ImportConfigDialog(QtWidgets.QDialog):

    def __init__(self, import_zip, graphics_scene, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ImportConfigDialog()
        self._ui.setupUi(self)

        self._import_zip = import_zip
        self._graphics_scene = graphics_scene
        self._workflow_scene = self._graphics_scene.workflowScene()
        self._undo_stack = self._graphics_scene.getUndoStack()

        self._step_map = None
        self._setup_step_map()
        self._setup_grid_layout()

        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonImport.clicked.connect(self._import_clicked)

    def _setup_step_map(self):
        # Get project information for the imported workflow.
        with zipfile.ZipFile(self._import_zip, mode="r") as archive:
            with tempfile.TemporaryDirectory() as temp_dir:
                archive.extract(DEFAULT_WORKFLOW_PROJECT_FILENAME, temp_dir)
                import_proj = QtCore.QSettings(os.path.join(temp_dir, DEFAULT_WORKFLOW_PROJECT_FILENAME), QtCore.QSettings.IniFormat)

        import_version = import_proj.value('version')
        import_proj.beginGroup('nodes')
        node_count = import_proj.beginReadArray('nodelist')
        import_steps = numpy.empty(shape=(node_count,), dtype=[("ID", "<U64"), ("Name", "<U64")])
        for i in range(node_count):
            import_proj.setArrayIndex(i)
            import_steps[i]["ID"] = import_proj.value('identifier')
            import_steps[i]["Name"] = import_proj.value('name')

        # Get workflow information.
        node_count = len([_ for _ in self._workflow_scene.items() if (_.Type == MetaStep.Type)])
        workflow_steps = numpy.empty(shape=(node_count,), dtype=[("ID", "<U64"), ("Name", "<U64")])
        i = 0
        for workflowitem in list(self._workflow_scene.items()):
            if workflowitem.Type == MetaStep.Type:
                workflow_steps[i]["ID"] = workflowitem.getIdentifier()
                workflow_steps[i]["Name"] = workflowitem.getName()
                i += 1

        # Check for version compatibility.
        if import_version != app_version.__version__:
            QtWidgets.QMessageBox.warning(self, 'Different Workflow Versions', f'The version of the imported workflow ({import_version})'
                                          f' does not match the version of the MAP Client ({app_version.__version__}).')

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

    def _import_clicked(self):
        self._update_step_map()

        # Import the new configurations into the workflow steps.
        step_dict = {}
        node_dict = {}
        for node in self._graphics_scene.items():
            if hasattr(node, 'Type') and node.Type == Node.Type:
                identifier = node.metaItem().getIdentifier()
                step = node.metaItem().getStep()
                step_dict[identifier] = step
                node_dict[identifier] = node

        with zipfile.ZipFile(self._import_zip, mode="r") as archive:
            with tempfile.TemporaryDirectory() as temp_dir:
                self._undo_stack.beginMacro('Import Configurations')
                archive.extractall(temp_dir)
                for row_index in range(len(self._step_map)):
                    current_text = self._step_map[row_index]["Selected"]
                    if current_text != '':
                        identifier = self._step_map[row_index]["ID"]

                        self._graphics_scene.setConfigureNode(node_dict[identifier])

                        configuration = loadConfiguration(temp_dir, identifier)
                        step_dict[identifier].deserialize(configuration)

                        for additional_cfg_file in step_dict[identifier].getAdditionalConfigFiles():
                            # TODO: Load any additional configuration files.
                            pass

                        # This method adds the change in configuration to the undo-redo stack.
                        self._graphics_scene.stepConfigured()
                self._undo_stack.endMacro()

        QtWidgets.QMessageBox.information(self, "Configurations Imported",
                                          "The selected configurations have been successfully imported.")
