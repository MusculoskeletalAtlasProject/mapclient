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
import logging
import shutil
import glob
import zipfile

from PySide6 import QtCore, QtWidgets, QtGui

from requests.exceptions import HTTPError

from mapclient.core.utils import get_steps_additional_config_files
from mapclient.exceptions import ClientRuntimeError

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, DEFAULT_WORKFLOW_ANNOTATION_FILENAME
from mapclient.view.dialogs.selfclosing.messagebox import MessageBox

from mapclient.view.utils import set_wait_cursor
from mapclient.view.utils import handle_runtime_error

from mapclient.view.workflow.ui.ui_workflowwidget import Ui_WorkflowWidget
from mapclient.view.workflow.workflowgraphicsscene import WorkflowGraphicsScene
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.view.managers.plugins.pluginupdater import PluginUpdater
from mapclient.tools.pmr.settings.general import PMR
from mapclient.settings.general import get_virtualenv_directory
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.settings.definitions import SHOW_STEP_NAMES, CLOSE_AFTER, USE_EXTERNAL_GIT, PREVIOUS_WORKFLOW

from mapclient.core.workflow.workflowitems import MetaStep
from mapclient.view.workflow.importconfigdialog import ImportConfigDialog

logger = logging.getLogger(__name__)


class WorkflowWidget(QtWidgets.QWidget):

    def __init__(self, mainWindow):
        QtWidgets.QWidget.__init__(self, parent=mainWindow)
        self._main_window = mainWindow
        self._ui = Ui_WorkflowWidget()
        self._ui.setupUi(self)

        self._pluginUpdater = PluginUpdater()

        self._undoStack = QtGui.QUndoStack(self)

        self._workflowManager = self._main_window.model().workflowManager()
        self._graphicsScene = WorkflowGraphicsScene(self)

        self._ui.graphicsView.setScene(self._graphicsScene)
        self._ui.graphicsView.setMainWindow(mainWindow)

        self._ui.graphicsView.setUndoStack(self._undoStack)
        self._graphicsScene.setUndoStack(self._undoStack)

        self._graphicsScene.setWorkflowScene(self._workflowManager.scene())

        self.action_Close = None  # Keep a handle to this for modifying the Ui.
        self._action_annotation = self._main_window.findChild(QtGui.QAction, "actionAnnotation")
        self._create_menu_items()

        model = self._workflowManager.getFilteredStepModel()
        self._ui.stepTreeView.setModel(model)

        self.updateStepTree()
        self.applyOptions()

        self._update_ui()

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditFilter.textChanged.connect(self._filter_text_changed)
        self._graphicsScene.selectionChanged.connect(self._ui.graphicsView.selectionChanged)
        self._ui.executeButton.clicked.connect(self.executeWorkflow)
        self._undoStack.indexChanged.connect(self.undoStackIndexChanged)

    def model(self):
        return self._main_window.model()

    def _filter_text_changed(self, text):
        reg_exp = QtCore.QRegularExpression(text, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
        self._ui.stepTreeView.setFilterRegularExpression(reg_exp)

    def _update_ui(self):
        if hasattr(self, '_main_window'):
            try:
                wfm = self._main_window.model().workflowManager()
                self._main_window.setWindowTitle(wfm.title())
            except RuntimeError:
                return

            widget_visible = self.isVisible()

            workflow_open = wfm.isWorkflowOpen()
            workflow_has_steps = wfm.isWorkflowPopulated()
            workflow_tracked = wfm.isWorkflowTracked()
            self.action_Close.setEnabled(workflow_open and widget_visible)
            self.setEnabled(workflow_open and widget_visible)
            self.action_Save.setEnabled(wfm.isModified() and widget_visible)
            self.action_SaveAs.setEnabled(widget_visible)
            self._action_annotation.setEnabled(workflow_open and widget_visible)
            self.action_New.setEnabled(widget_visible)
            self.action_NewPMR.setEnabled(widget_visible)
            self.action_Open.setEnabled(widget_visible)
            self.action_Execute.setEnabled(workflow_open and widget_visible)
            # self.action_Continue.setEnabled(workflow_open and not widget_visible)
            self.action_Reverse.setEnabled(workflow_open and not widget_visible)
            self.action_Abort.setEnabled(workflow_open and not widget_visible)
            self.action_Import_CFG.setEnabled(workflow_open and widget_visible and workflow_has_steps)
            self.action_Export_CFG.setEnabled(workflow_open and widget_visible and workflow_has_steps)
            self.action_ZoomIn.setEnabled(widget_visible)

    def updateStepTree(self):
        self._ui.stepTreeView.expandAll()

    def applyOptions(self):
        om = self._main_window.model().optionsManager()
        show_step_names = om.getOption(SHOW_STEP_NAMES)
        self._graphicsScene.showStepNames(show_step_names)

    def undoStackIndexChanged(self, index):
        self._main_window.model().workflowManager().undoStackIndexChanged(index)
        self._update_ui()

    def undoRedoStack(self):
        return self._undoStack

    def showEvent(self, *args, **kwargs):
        self._update_ui()
        return QtWidgets.QWidget.showEvent(self, *args, **kwargs)

    def hideEvent(self, *args, **kwargs):
        self._update_ui()
        return QtWidgets.QWidget.hideEvent(self, *args, **kwargs)

    @handle_runtime_error
    def _abort_execution(self):
        self._main_window.abort_execution()

    @handle_runtime_error
    def executeNext(self):
        try:
            self._main_window.execute()
        except WorkflowError as e:
            raise ClientRuntimeError('Error in workflow execution', str(e))

    def executeWorkflow(self):
        wfm = self._main_window.model().workflowManager()
        errors = []

        if wfm.isModified():
            errors.append('The workflow has not been saved.')

        status = wfm.canExecute()
        if status == 1:
            errors.append('Not all steps in the workflow have been successfully configured.')
        elif status == 2:
            errors.append('The workflow is empty.')
        elif status == 3:
            errors.append('The workflow has multiple steps but no connections.')
        elif status == 4:
            errors.append('The workflow is currently running.')
        elif status == 5:
            errors.append('The workflow has a loop.')

        if errors:
            errors_str = '\n'.join(
                ['  %d. %s' % (i + 1, e) for i, e in enumerate(errors)])
            error_msg = ('The workflow could not be executed for the '
                         'following reason%s:\n\n%s' % (
                             len(errors) > 1 and 's' or '', errors_str,
                         ))
            QtWidgets.QMessageBox.critical(self, 'Workflow Execution', error_msg, QtWidgets.QMessageBox.Ok)
        else:
            wfm.register_finished_workflow_callback(self._workflow_finished)
            self.executeNext()

    def continueWorkflow(self):
        self.executeNext()

    def _abort_workflow(self):
        self._abort_execution()
        self._reset_workflow_direction()

    def _reverse_workflow_direction(self):
        self._main_window.set_workflow_direction(not self.action_Reverse.isChecked())

    def _reset_workflow_direction(self):
        self.action_Reverse.setChecked(False)
        self._main_window.set_workflow_direction(True)

    def identifierOccursCount(self, identifier):
        return self._main_window.model().workflowManager().identifierOccursCount(identifier)

    def setCurrentWidget(self, widget):
        self._main_window.set_current_widget(widget)

    def setWidgetUndoRedoStack(self, stack):
        self._main_window.set_current_undo_redo_stack(stack)

    def new(self, pmr=False):
        self.close()

        workflowDir = self._get_workflow_dir()
        if workflowDir:
            self._create_new_workflow(workflowDir, pmr)

    def _workflow_finished(self, successfully):
        if successfully:
            close_after = self._main_window.model().optionsManager().getOption(CLOSE_AFTER)
            mb = MessageBox(QtWidgets.QMessageBox.Icon.Information, "Workflow Finished",
                            "Workflow finished successfully.",
                            QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Default,
                            parent=self._main_window,
                            close_after=close_after)
            mb.setIconPixmap(QtGui.QPixmap(":/mapclient/images/green_tick.png").scaled(64, 64))
            mb.exec()
        else:
            self._reset_workflow_direction()

    def _get_workflow_dir(self):
        m = self._main_window.model().workflowManager()
        workflow_dir = QtWidgets.QFileDialog.getExistingDirectory(self._main_window, caption='Select Workflow Directory', dir=m.previousLocation())
        if workflow_dir is None:
            # user abort
            return ''

        class ProblemClass:
            mk_workflow_dir = False
            rm_tree_success = True

            @staticmethod
            def rm_tree_unsuccessful(_one, _two, _three):
                ProblemClass.rm_tree_success = False

        if m.exists(workflow_dir):
            # Check to make sure user wishes to overwrite existing workflow.
            ret = QtWidgets.QMessageBox.warning(
                self, 'Replace Existing Workflow', 'A Workflow already exists at this location.  Do you want to replace this Workflow?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if ret == QtWidgets.QMessageBox.StandardButton.No:
                # user abort
                return ''
            else:
                # Delete contents of directory
                shutil.rmtree(workflow_dir, onerror=ProblemClass.rm_tree_unsuccessful)
                ProblemClass.mk_workflow_dir = True

        # got dir, continue
        if ProblemClass.rm_tree_success:
            if ProblemClass.mk_workflow_dir:
                os.mkdir(workflow_dir)

            return workflow_dir
        else:
            QtWidgets.QMessageBox.warning(self,
                                          'Replace Existing Workflow',
                                          'Could not remove existing workflow,'
                                          'New workflow not created.',
                                          QtWidgets.QMessageBox.StandardButton.Ok)

        return ''

    @handle_runtime_error
    @set_wait_cursor
    def _create_new_workflow(self, workflow_dir, pmr):
        m = self._main_window.model().workflowManager()
        om = self._main_window.model().optionsManager()
        m.new(workflow_dir)
        m.setPreviousLocation(workflow_dir)

        if pmr:
            pmr_info = PMR()
            pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
            if pmr_tool.has_access():
                dir_name = os.path.basename(workflow_dir)
                try:
                    repourl = pmr_tool.addWorkspace('Workflow: ' + dir_name, None)
                    pmr_tool.linkWorkspaceDirToUrl(workflow_dir, repourl)
                except HTTPError as e:
                    logger.exception('Error creating new')
                    self.close()
                    raise ClientRuntimeError(
                        'Error Creating New', e)
            else:
                raise ClientRuntimeError('Error Creating New', "Client doesn't have access to PMR")

        self._undoStack.clear()
        self._ui.graphicsView.setLocation(workflow_dir)
        self._graphicsScene.update_model()
        self._update_ui()

    def newpmr(self):
        self.new(pmr=True)

    def open(self):
        wm = self._main_window.model().workflowManager()

        primary_filter = f"Workflow configuration file ({DEFAULT_WORKFLOW_PROJECT_FILENAME})"

        workflow_conf = QtWidgets.QFileDialog.getOpenFileName(
            self._main_window,
            caption='Open Workflow',
            dir=os.path.join(wm.previousLocation(), DEFAULT_WORKFLOW_PROJECT_FILENAME),
            filter=f"{primary_filter};;Any file (*.*)",
            selectedFilter=primary_filter,
            options=(
                    QtWidgets.QFileDialog.Option.DontResolveSymlinks |
                    QtWidgets.QFileDialog.Option.ReadOnly
            )
        )[0]

        if workflow_conf:
            # Remove the filename to get the directory.
            workflow_dir = os.path.dirname(workflow_conf)

            if wm.is_restricted(workflow_dir):
                QtWidgets.QMessageBox.warning(
                    self._main_window, 'Workflow in use',
                    'Another instance of the MAP Client is already using this workflow and '
                    'only one instance of a workflow may be opened at a time.'
                    ' Please try opening a different workflow.',
                    QtWidgets.QMessageBox.StandardButton.Ok,
                    QtWidgets.QMessageBox.StandardButton.Ok)
            else:
                err = self.openWorkflow(workflow_dir)
                if err:
                    QtWidgets.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + err)

    def openWorkflow(self, workflow_dir):
        result = ''
        if len(workflow_dir):
            try:
                logger.info('Performing workflow checks on open ...')
                self.performWorkflowChecks(workflow_dir)
                self._load(workflow_dir)
            except (ValueError, WorkflowError) as e:
                logger.error('Invalid Workflow.  ' + str(e))
                result = str(e)
            except ResourceWarning as e:
                logger.warning(e)

        return result

    def showDownloadableContent(self, plugins=None, dependencies=None):
        from mapclient.view.managers.plugins.plugindownloader import PluginDownloader
        dlg = PluginDownloader(self)
        dlg.fillPluginTable(plugins)
        dlg.fillDependenciesTable(dependencies)
        dlg.setModal(True)
        if dlg.exec():
            return dlg.downloadDependencies(), dlg.installMissingPlugins()

        return False, False

    def installMissingPlugins(self, plugins):
        from mapclient.view.managers.plugins.pluginprogress import PluginProgress
        directory = QtWidgets.QFileDialog.getExistingDirectory(caption='Select Plugin Directory', dir='',
                                                               options=QtWidgets.QFileDialog.Option.ShowDirsOnly |
                                                                       QtWidgets.QFileDialog.Option.DontResolveSymlinks)
        if directory:
            pm = self._main_window.model().getPluginManager()
            pluginDirs = pm.directories()
            if directory not in pluginDirs:
                pluginDirs.append(directory)
                pm.setDirectories(pluginDirs)
        self.dlg = PluginProgress(plugins, directory, self)
        self.dlg.show()
        self.dlg.run()

    def installMissingDependencies(self, plugin_dependencies):
        dependencies = []
        for plugin in plugin_dependencies:
            for dependency in plugin_dependencies[plugin]:
                if dependency not in dependencies:
                    dependencies += [dependency]
        unsuccessful_installs = self.pipInstallDependency(dependencies)
        return unsuccessful_installs

    def pipInstallDependency(self, dependencies):
        from mapclient.view.managers.plugins.dependencyinstallation import InstallDependencies
        self.installer = InstallDependencies(dependencies, get_virtualenv_directory())
        self.installer.show()
        unsuccessful_installs = self.installer.run()
        self.installer.close()
        if list(unsuccessful_installs.keys()):
            QtWidgets.QMessageBox.critical(self, 'Failed Installation',
                                           'One or more of the required dependencies could not be installed.'
                                           '\nPlease refer to the program logs for more information.',
                                           QtWidgets.QMessageBox.Ok)
        return unsuccessful_installs

    def getMissingDependencies(self, dependencies):
        """
        Determine which dependencies are missing from the given dependencies list.
        """
        virtenv_dir = get_virtualenv_directory()

        virtenv_exists = os.path.exists(os.path.join(virtenv_dir, 'bin'))
        required_dependencies = []
        if not virtenv_exists:
            if self.setupVEQuery():
                if self.setupMAPClientVirtEnv(virtenv_dir):
                    required_dependencies = self.getRequiredDependencies(dependencies)
        else:
            required_dependencies = self.getRequiredDependencies(dependencies)
        return required_dependencies

    def performWorkflowChecks(self, workflow_dir):
        """
        Perform workflow checks
         1. Check plugins
         2. Check dependencies
         3. Get missing plugins
         4. Get missing dependencies
         5. Check for errors
         6. Update step tree
        """
        #         wm = self._mainWindow.model().workflowManager()
        pm = self._main_window.model().pluginManager()
        steps_to_install = pm.checkPlugins(workflow_dir)
        dependencies_to_install = pm.checkDependencies(workflow_dir)
        if steps_to_install or dependencies_to_install:
            download_dependencies, download_plugins = self.showDownloadableContent(plugins=steps_to_install, dependencies=dependencies_to_install)
            if download_dependencies:
                self.installMissingDependencies(dependencies_to_install)
            if download_plugins:
                self.installMissingPlugins(steps_to_install)

        #         pm = self._mainWindow.model().pluginManager()
        #         pm.load()
        if pm.haveErrors():
            self._main_window._show_plugin_errors_dialog()
            self.updateStepTree()

    @handle_runtime_error
    @set_wait_cursor
    def _load(self, workflow_dir):
        try:
            m = self._main_window.model().workflowManager()
            m.load(workflow_dir, self._graphicsScene.sceneRect())
            m.setPreviousLocation(workflow_dir)
            self._graphicsScene.update_model()
            self._ui.graphicsView.setLocation(workflow_dir)
            self._update_ui()
        except:
            self.close()
            raise

        om = self._main_window.model().optionsManager()
        om.setOption(PREVIOUS_WORKFLOW, workflow_dir)

    def reload(self):
        m = self._main_window.model().workflowManager()
        self._load(m.location())

    def close(self):
        self._main_window.confirm_close()
        m = self._main_window.model().workflowManager()
        self._undoStack.clear()
        self._graphicsScene.clear()
        m.close()
        self._update_ui()

    def save(self):
        m = self._main_window.model().workflowManager()
        location_set = os.path.exists(m.location())
        if location_set:
            self._updateLocation()
        else:
            location_set = self._set_location()
        if location_set:
            m.scene().setViewParameters(self._ui.graphicsView.getViewParameters())
            m.save()
            if self.commitChanges(m.location()):
                self._setIndexerFile(m.location())
            else:
                pass  # undo changes

        self._update_ui()

    def saveAs(self):
        wm = self._main_window.model().workflowManager()
        workflow_dir = wm.location()
        location_set = self._set_location()
        if location_set:
            self.save()
            src_git_dir = os.path.join(workflow_dir, '.git')
            if os.path.isdir(src_git_dir):
                shutil.copytree(src_git_dir, os.path.join(wm.location(), '.git'), dirs_exist_ok=True)

    def _updateLocation(self):
        m = self._main_window.model().workflowManager()
        workflow_dir = m.location()
        if m.set_location(workflow_dir):
            self._ui.graphicsView.setLocation(workflow_dir)
            self._graphicsScene.update_model()

    def _set_location(self):
        location_set = False
        m = self._main_window.model().workflowManager()
        workflow_dir = self._get_workflow_dir()
        if workflow_dir:
            m.setPreviousLocation(workflow_dir)
            m.set_location(workflow_dir)
            self._ui.graphicsView.setLocation(workflow_dir)
            self._graphicsScene.update_model()
            location_set = True

        return location_set

    def commitChanges(self, workflowDir):
        om = self._main_window.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
        if not pmr_tool.is_pmr_workflow(workflowDir):
            # nothing to commit.
            return True

        return self._commitChanges(workflowDir, 'Workflow saved.')

    @handle_runtime_error
    @set_wait_cursor
    def _commitChanges(self, workflowDir, comment, commit_local=False):
        committed_changes = False
        om = self._main_window.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
        try:
            # If the user has added a .gitignore to the workflow root directory, let this automatically filter the files that are committed.
            if os.path.isfile(os.path.join(workflowDir, ".gitignore")):
                workflow_files = [workflowDir, ]
            else:
                workflow_files = [workflowDir + '/%s' % (DEFAULT_WORKFLOW_PROJECT_FILENAME),
                                  workflowDir + '/%s' % (DEFAULT_WORKFLOW_ANNOTATION_FILENAME)]
                for f in os.listdir(workflowDir):
                    if f.endswith(".conf"):
                        full_filename = os.path.join(workflowDir, f)
                        if full_filename not in workflow_files:
                            workflow_files.append(full_filename)

                self._workflowManager.scene()
                for item in self._workflowManager.scene().items():
                    if item.Type == MetaStep.Type:
                        workflow_files.extend(get_steps_additional_config_files(item.getStep()))

            pmr_tool.commit_files(workflowDir, comment, workflow_files)
            if not commit_local:
                pmr_tool.pushToRemote(workflowDir)
            committed_changes = True
        except ClientRuntimeError:
            # handler will deal with this.
            raise
        except Exception:
            logger.exception('Error')
            raise ClientRuntimeError(
                'Error Saving', 'The commit to PMR did not succeed')

        return committed_changes

    @handle_runtime_error
    @set_wait_cursor
    def _setIndexerFile(self, workflow_dir):
        om = self._main_window.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))

        if not pmr_tool.is_pmr_workflow(workflow_dir):
            return
        try:
            pmr_tool.addFileToIndexer(workflow_dir, DEFAULT_WORKFLOW_ANNOTATION_FILENAME)
        #             pmr_tool.commitFiles(local_workspace_dir, message, files)
        except ClientRuntimeError:
            # handler will deal with this.
            raise

    @staticmethod
    def _set_action_properties(action, name, slot, shortcut='', statustip=''):
        action.setObjectName(name)
        action.triggered.connect(slot)
        if len(shortcut) > 0:
            action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setStatusTip(statustip)

    def zoom_in(self):
        self._ui.graphicsView.zoom_in()

    def zoom_out(self):
        self._ui.graphicsView.zoom_out()

    def reset_zoom(self):
        self._ui.graphicsView.reset_zoom()

    def import_cfg(self):
        m = self._main_window.model().workflowManager()
        import_source, _ = QtWidgets.QFileDialog.getOpenFileName(self._main_window, caption='Select Import File', dir=m.previousLocation(),
                                                                 filter=f"Data files(*.zip);;MAP Client Project file({DEFAULT_WORKFLOW_PROJECT_FILENAME})")

        if len(import_source) > 0:
            dlg = ImportConfigDialog(import_source, self._graphicsScene, self)
            if dlg.is_compatible():
                dlg.setModal(True)
                dlg.exec()

    def export_cfg(self):
        self.save()

        m = self._main_window.model().workflowManager()
        workflow_dir = m.location()

        if self._workflowManager.location():
            workflow_name = os.path.basename(self._workflowManager.location())
        else:
            workflow_name = "workflow"
        default_location = os.path.join(m.previousLocation(), f"{workflow_name}-config")
        export_zip, _ = QtWidgets.QFileDialog.getSaveFileName(self._main_window, caption='Select Export File', dir=default_location,
                                                              filter="Data files(*.zip)")

        # Select only .proj and .conf files.
        os.chdir(workflow_dir)
        types = ('*.proj', '*.conf')
        cfg_files = []
        for files in types:
            cfg_files.extend(glob.glob(files))

        def _workflow_relative_path(filename):
            return os.path.relpath(filename, workflow_dir)

        # Check the workflow-steps for additional config files.
        for workflow_item in list(m.scene().items()):
            if workflow_item.Type == MetaStep.Type:
                additional_config_files = workflow_item.getStep().getAdditionalConfigFiles()
                cfg_files.extend([_workflow_relative_path(file) for file in additional_config_files])

        # Zip files and store in export destination.
        if export_zip:
            with zipfile.ZipFile(export_zip, mode="w") as archive:
                for file in cfg_files:
                    archive.write(file)

    def _create_menu_items(self):
        menu_file = self._main_window.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_File')
        menu_workflow = self._main_window.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_Workflow')
        menu_view = self._main_window.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_View')

        last_view_menu_action = menu_view.actions()[-1]
        last_file_menu_action = menu_file.actions()[-1]

        menu_new = QtWidgets.QMenu('&New', menu_file)
        #        menu_Open = QtGui.QMenu('&Open', menu_File)

        self.action_NewPMR = QtGui.QAction('PMR Workflow', menu_new)
        self._set_action_properties(self.action_NewPMR, 'action_NewPMR', self.newpmr, 'Ctrl+Shift+N',
                                    'Create a new PMR based Workflow')
        self.action_New = QtGui.QAction('Workflow', menu_new)
        self._set_action_properties(self.action_New, 'action_New', self.new, 'Ctrl+N', 'Create a new Workflow')
        self.action_Open = QtGui.QAction('&Open', menu_file)
        self._set_action_properties(self.action_Open, 'action_Open', self.open, 'Ctrl+O', 'Open an existing Workflow')
        self.action_Import_CFG = QtGui.QAction('Import Config', menu_workflow)
        self._set_action_properties(self.action_Import_CFG, 'action_Import_CFG', self.import_cfg, '',
                                    'Import workflow configuration from file')
        self.action_Export_CFG = QtGui.QAction('Export Config', menu_workflow)
        self._set_action_properties(self.action_Export_CFG, 'action_Export_CFG', self.export_cfg, '',
                                    'Export workflow configuration to file')
        self.action_Close = QtGui.QAction('&Close', menu_file)
        self._set_action_properties(self.action_Close, 'action_Close', self.close, 'Ctrl+W', 'Close open Workflow')
        self.action_Save = QtGui.QAction('&Save', menu_file)
        self._set_action_properties(self.action_Save, 'action_Save', self.save, 'Ctrl+S', 'Save Workflow')
        self.action_SaveAs = QtGui.QAction('Save As', menu_file)
        self._set_action_properties(self.action_SaveAs, 'action_SaveAs', self.saveAs, '', 'Save Workflow as ...')
        self.action_Execute = QtGui.QAction('E&xecute', menu_workflow)
        self._set_action_properties(self.action_Execute, 'action_Execute', self.executeWorkflow, 'Ctrl+X',
                                    'Execute Workflow')
        # self.action_Continue = QtGui.QAction('&Continue', menu_workflow)
        # self._set_action_properties(self.action_Continue, 'action_Continue', self.continueWorkflow, 'Ctrl+T',
        #                             'Continue executing Workflow')
        self.action_Reverse = QtGui.QAction('Reverse', menu_workflow)
        self.action_Reverse.setCheckable(True)
        self._set_action_properties(self.action_Reverse, 'action_Reverse', self._reverse_workflow_direction, '',
                                    'Reverse Workflow Direction')
        self.action_Abort = QtGui.QAction('Abort', menu_workflow)
        self._set_action_properties(self.action_Abort, 'action_Abort', self._abort_workflow, '',
                                    'Abort Workflow')

        self.action_ZoomIn = QtGui.QAction('Zoom In', menu_view)
        self._set_action_properties(self.action_ZoomIn, 'action_ZoomIn', self.zoom_in, 'Ctrl++',
                                    'Zoom in Workflow')
        self.action_ZoomOut = QtGui.QAction('Zoom Out', menu_view)
        self._set_action_properties(self.action_ZoomOut, 'action_ZoomOut', self.zoom_out, 'Ctrl+-',
                                    'Zoom out Workflow')
        self.action_ResetZoom = QtGui.QAction('Reset Zoom', menu_view)
        self._set_action_properties(self.action_ResetZoom, 'action_ResetZoom', self.reset_zoom, '',
                                    'Reset Workflow Zoom')

        menu_new.insertAction(QtGui.QAction(self), self.action_New)
        menu_new.insertAction(QtGui.QAction(self), self.action_NewPMR)

        menu_file.insertMenu(last_file_menu_action, menu_new)
        menu_file.insertAction(last_file_menu_action, self.action_Open)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Save)
        menu_file.insertAction(last_file_menu_action, self.action_SaveAs)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Import_CFG)
        menu_file.insertAction(last_file_menu_action, self.action_Export_CFG)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Close)
        menu_file.insertSeparator(last_file_menu_action)

        menu_view.addAction(self.action_ZoomIn)
        menu_view.addAction(self.action_ZoomOut)
        menu_view.addAction(self.action_ResetZoom)
        menu_view.insertSeparator(last_view_menu_action)

        menu_workflow.addAction(self.action_Execute)
        # menu_workflow.addAction(self.action_Continue)
        menu_workflow.addAction(self.action_Reverse)
        menu_workflow.addAction(self.action_Abort)
