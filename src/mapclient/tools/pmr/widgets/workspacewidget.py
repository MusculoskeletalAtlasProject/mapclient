import os
import logging

from PySide6 import QtWidgets

from mapclient.settings.definitions import USE_EXTERNAL_GIT
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.view.utils import set_wait_cursor
from mapclient.view.utils import handle_runtime_error
from mapclient.tools.pmr.settings.general import PMR
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.importworkflowdialog import ImportWorkflowDialog

logger = logging.getLogger(__name__)


class WorkspaceWidget(QtWidgets.QWidget):

    def __init__(self, workflow_widget, parent=None):
        super().__init__(parent)

        self._workflow_widget = workflow_widget
        self._use_external_git = workflow_widget

        self._setup_ui()
        self._make_connections()

    def _setup_ui(self):
        self._import_button = QtWidgets.QPushButton("Import")
        import_layout = QtWidgets.QHBoxLayout()
        import_layout.addWidget(self._import_button)
        import_layout.addStretch(1)

        self._update_button = QtWidgets.QPushButton("Update")
        update_layout = QtWidgets.QHBoxLayout()
        update_layout.addWidget(self._update_button)
        update_layout.addStretch(1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(import_layout)
        layout.addLayout(update_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def _make_connections(self):
        self._import_button.clicked.connect(self.import_from_pmr)
        self._update_button.clicked.connect(self.update_from_pmr)

    def import_from_pmr(self):
        m = self._workflow_widget.model().workflowManager()
        dlg = ImportWorkflowDialog(m.previousLocation(), self._use_external_git, self)

        if dlg.exec():
            destination_dir = dlg.destinationDir()
            workspace_url = dlg.workspaceUrl()
            if os.path.exists(destination_dir) and workspace_url:
                try:
                    self._clone_from_pmr(workspace_url, destination_dir)
                    logger.info('Perform workflow checks on import ...')
                    self._workflow_widget.performWorkflowChecks(destination_dir)
                    self._workflow_widget._load(destination_dir)
                except (ValueError, WorkflowError) as e:
                    logger.error('Invalid Workflow.  ' + str(e))
                    QtWidgets.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + str(e))

    def update_from_pmr(self):
        if self._update_from_pmr():
            self._workflow_widget.reload()
        else:
            logger.error('Attempt to update workflow failed.')
            QtWidgets.QMessageBox.warning(self, 'Invalid workflow', 'This workflow cannot be updated.')

    @handle_runtime_error
    @set_wait_cursor
    def _update_from_pmr(self):
        m = self._workflow_widget.model().workflowManager()
        om = self._workflow_widget.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
        workflow_dir = m.location()
        if pmr_tool.is_pmr_workflow(workflow_dir):
            pmr_tool.pullFromRemote(workflow_dir)
            return True

        return False

    @handle_runtime_error
    @set_wait_cursor
    def _clone_from_pmr(self, workspace_url, workflow_dir):
        om = self._workflow_widget.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))

        pmr_tool.cloneWorkspace(
            remote_workspace_url=workspace_url,
            local_workspace_dir=workflow_dir,
        )
