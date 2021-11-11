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

from PySide2 import QtCore, QtWidgets, QtGui

from requests.exceptions import HTTPError
from mapclient.exceptions import ClientRuntimeError

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, \
    DEFAULT_WORKFLOW_ANNOTATION_FILENAME

from mapclient.view.utils import set_wait_cursor
from mapclient.view.utils import handle_runtime_error

from mapclient.view.workflow.ui.ui_workflowwidget import Ui_WorkflowWidget
from mapclient.view.workflow.workflowgraphicsscene import WorkflowGraphicsScene
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.view.importworkflowdialog import ImportWorkflowDialog
from mapclient.view.managers.plugins.pluginupdater import PluginUpdater
from mapclient.tools.pmr.settings.general import PMR
from mapclient.settings.general import get_virtualenv_directory
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.settings.definitions import SHOW_STEP_NAMES, USE_EXTERNAL_GIT, PREVIOUS_WORKFLOW

logger = logging.getLogger(__name__)


class WorkflowWidget(QtWidgets.QWidget):

    def __init__(self, mainWindow):
        QtWidgets.QWidget.__init__(self, parent=mainWindow)
        self._mainWindow = mainWindow
        self._ui = Ui_WorkflowWidget()
        self._ui.setupUi(self)

        self._pluginUpdater = PluginUpdater()

        self._undoStack = QtWidgets.QUndoStack(self)

        self._workflowManager = self._mainWindow.model().workflowManager()
        self._graphicsScene = WorkflowGraphicsScene(self)

        self._ui.graphicsView.setScene(self._graphicsScene)
        self._ui.graphicsView.setMainWindow(mainWindow)

        self._ui.graphicsView.setUndoStack(self._undoStack)
        self._graphicsScene.setUndoStack(self._undoStack)

        self._graphicsScene.setWorkflowScene(self._workflowManager.scene())

        self.action_Close = None  # Keep a handle to this for modifying the Ui.
        self._action_annotation = self._mainWindow.findChild(QtWidgets.QAction, "actionAnnotation")
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

    def _filter_text_changed(self, text):
        reg_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
#         self._workflowManager.getFilteredStepModel().setFilterRegExp(reg_exp)
        self._ui.stepTreeView.setFilterRegExp(reg_exp)

    def _update_ui(self):
        if hasattr(self, '_mainWindow'):
            try:
                wfm = self._mainWindow.model().workflowManager()
                self._mainWindow.setWindowTitle(wfm.title())
            except RuntimeError:
                return

            widget_visible = self.isVisible()

            workflow_open = wfm.isWorkflowOpen()
            workflow_tracked = wfm.isWorkflowTracked()
            self.action_Close.setEnabled(workflow_open and widget_visible)
            self.setEnabled(workflow_open and widget_visible)
            self.action_Save.setEnabled(wfm.isModified() and widget_visible)
            self.action_SaveAs.setEnabled(widget_visible)
            self._action_annotation.setEnabled(workflow_open and widget_visible)
            self.action_Import.setEnabled(widget_visible)
            self.action_Update.setEnabled(workflow_tracked)
            self.action_New.setEnabled(widget_visible)
            self.action_NewPMR.setEnabled(widget_visible)
            self.action_Open.setEnabled(widget_visible)
            self.action_Execute.setEnabled(workflow_open and widget_visible)
            self.action_Continue.setEnabled(workflow_open and not widget_visible)
            self.action_ZoomIn.setEnabled(widget_visible)

    def updateStepTree(self):
        self._ui.stepTreeView.expandAll()

    def applyOptions(self):
        om = self._mainWindow.model().optionsManager()
        show_step_names = om.getOption(SHOW_STEP_NAMES)
        self._graphicsScene.showStepNames(show_step_names)
        # self._ui.graphicsView.showStepNames(show_step_names)

    def undoStackIndexChanged(self, index):
        self._mainWindow.model().workflowManager().undoStackIndexChanged(index)
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
    def executeNext(self):
        try:
            self._mainWindow.execute()
        except WorkflowError as e:
            raise ClientRuntimeError('Error in workflow execution', str(e))

    def executeWorkflow(self):
        wfm = self._mainWindow.model().workflowManager()
        errors = []

        if wfm.isModified():
            errors.append('The workflow has not been saved.')

        if not wfm.canExecute():
            errors.append('Not all steps in the workflow have been '
                'successfully configured.')

        if not errors:
            self.executeNext()
#             self._mainWindow.execute()  # .model().workflowManager().execute()
        else:
            errors_str = '\n'.join(
                ['  %d. %s' % (i + 1, e) for i, e in enumerate(errors)])
            error_msg = ('The workflow could not be executed for the '
                'following reason%s:\n\n%s' % (
                    len(errors) > 1 and 's' or '', errors_str,
            ))
            QtWidgets.QMessageBox.critical(self, 'Workflow Execution', error_msg, QtWidgets.QMessageBox.Ok)

    def continueWorkflow(self):
        self.executeNext()

    def identifierOccursCount(self, identifier):
        return self._mainWindow.model().workflowManager().identifierOccursCount(identifier)

    def setCurrentWidget(self, widget):
        self._mainWindow.set_current_widget(widget)

    def setWidgetUndoRedoStack(self, stack):
        self._mainWindow.set_current_undo_redo_stack(stack)

    def new(self, pmr=False):
        workflowDir = self._getWorkflowDir()
        if workflowDir:
            self._createNewWorkflow(workflowDir, pmr)

    def _getWorkflowDir(self):
        m = self._mainWindow.model().workflowManager()
        workflowDir = QtWidgets.QFileDialog.getExistingDirectory(self._mainWindow, caption='Select Workflow Directory', directory=m.previousLocation())
        if workflowDir is None:
            # user abort
            return ''

        class ProblemClass(object):
            mk_workflow_dir = False
            rm_tree_success = True

            def rm_tree_unsuccessful(self, _one, _two, _three):
                self.rm_tree_success = False

        if m.exists(workflowDir):
            # Check to make sure user wishes to overwrite existing workflow.
            ret = QtWidgets.QMessageBox.warning(self,
                                                'Replace Existing Workflow',
                                                'A Workflow already exists at this location.  '
                                                'Do you want to replace this Workflow?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            # (QtGui.QMessageBox.Warning, '')
            if ret == QtWidgets.QMessageBox.No:
                # user abort
                return ''
            else:
                # Delete contents of directory
                shutil.rmtree(workflowDir, onerror=ProblemClass.rm_tree_unsuccessful)
                ProblemClass.mk_workflow_dir = True

        # got dir, continue
        if ProblemClass.rm_tree_success:
            if ProblemClass.mk_workflow_dir:
                os.mkdir(workflowDir)

            return workflowDir
        else:
            QtWidgets.QMessageBox.warning(self,
                                          'Replace Existing Workflow',
                                          'Could not remove existing workflow,'
                                          'New workflow not created.',
                                          QtWidgets.QMessageBox.Ok)

        return ''

    @handle_runtime_error
    @set_wait_cursor
    def _createNewWorkflow(self, workflow_dir, pmr):
        m = self._mainWindow.model().workflowManager()
        om = self._mainWindow.model().optionsManager()
        m.new(workflow_dir)
        m.setPreviousLocation(workflow_dir)

        if pmr:
            pmr_info = PMR()
            pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
            if pmr_tool.hasAccess():
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
        self._graphicsScene.updateModel()
        self._update_ui()

    def newpmr(self):
        self.new(pmr=True)

    def open(self):
        m = self._mainWindow.model().workflowManager()

        primary_filter = f"Workflow configuration file ({DEFAULT_WORKFLOW_PROJECT_FILENAME})"

        workflow_conf = QtWidgets.QFileDialog.getOpenFileName(
            self._mainWindow,
            caption='Open Workflow',
            dir=os.path.join(m.previousLocation(), DEFAULT_WORKFLOW_PROJECT_FILENAME),
            filter=f"{primary_filter};;Any file (*.*)",
            selectedFilter=primary_filter,
            options=(
                QtWidgets.QFileDialog.DontResolveSymlinks |
                QtWidgets.QFileDialog.ReadOnly
            )
        )[0]

        if workflow_conf:
            # Remove the filename to get the directory.
            workflowDir = os.path.dirname(workflow_conf)

            err = self.openWorkflow(workflowDir)
            if err:
                QtWidgets.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + err)

    def openWorkflow(self, workflowDir):
        result = ''
        if len(workflowDir):
            try:
                logger.info('Performing workflow checks on open ...')
                self.performWorkflowChecks(workflowDir)
                self._load(workflowDir)
            except (ValueError, WorkflowError) as e:
                logger.error('Invalid Workflow.  ' + str(e))
                result = str(e)

        return result

    def showDownloadableContent(self, plugins={}, dependencies={}):
        from mapclient.view.managers.plugins.plugindownloader import PluginDownloader
        dlg = PluginDownloader(self)
        dlg.fillPluginTable(plugins)
        dlg.fillDependenciesTable(dependencies)
        dlg.setModal(True)
        if dlg.exec_():
            return dlg.downloadDependencies(), dlg.installMissingPlugins()

        return False, False

    def installMissingPlugins(self, plugins):
        from mapclient.view.managers.plugins.pluginprogress import PluginProgress
        directory = QtWidgets.QFileDialog.getExistingDirectory(caption='Select Plugin Directory', dir='',
                                                               options=QtWidgets.QFileDialog.ShowDirsOnly |
                                                                       QtWidgets.QFileDialog.DontResolveSymlinks)
        if directory:
            pm = self._mainWindow.model().getPluginManager()
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

    def performWorkflowChecks(self, workflowDir):
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
        pm = self._mainWindow.model().pluginManager()
        steps_to_install = pm.checkPlugins(workflowDir)
        dependencies_to_install = pm.checkDependencies(workflowDir)
        if steps_to_install or dependencies_to_install:
            download_dependencies, download_plugins = self.showDownloadableContent(plugins=steps_to_install, dependencies=dependencies_to_install)
            if download_dependencies:
                self.installMissingDependencies(dependencies_to_install)
            if download_plugins:
                self.installMissingPlugins(steps_to_install)

#         pm = self._mainWindow.model().pluginManager()
#         pm.load()
        if pm.haveErrors():
            self._mainWindow._show_plugin_errors_dialog()
            self.updateStepTree()

    def importFromPMR(self):
        m = self._mainWindow.model().workflowManager()
        dlg = ImportWorkflowDialog(m.previousLocation(), self._mainWindow)
        if dlg.exec_():
            destination_dir = dlg.destinationDir()
            workspace_url = dlg.workspaceUrl()
            if os.path.exists(destination_dir) and workspace_url:
                try:
                    self._cloneFromPMR(workspace_url, destination_dir)
                    logger.info('Perform workflow checks on import ...')
                    self.performWorkflowChecks(destination_dir)
                    self._load(destination_dir)
                except (ValueError, WorkflowError) as e:
                    logger.error('Invalid Workflow.  ' + str(e))
                    QtWidgets.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + str(e))

    def updateFromPMR(self):
        self._updateFromPMR()

    @handle_runtime_error
    @set_wait_cursor
    def _updateFromPMR(self):
        m = self._mainWindow.model().workflowManager()
        om = self._mainWindow.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))

        pmr_tool.pullFromRemote(m.location())

    @handle_runtime_error
    @set_wait_cursor
    def _cloneFromPMR(self, workspace_url, workflowDir):
        om = self._mainWindow.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))

        pmr_tool.cloneWorkspace(
            remote_workspace_url=workspace_url,
            local_workspace_dir=workflowDir,
        )

    @handle_runtime_error
    @set_wait_cursor
    def _load(self, workflow_dir):
        try:
            m = self._mainWindow.model().workflowManager()
            m.load(workflow_dir)
            m.setPreviousLocation(workflow_dir)
            self._graphicsScene.updateModel()
            self._ui.graphicsView.setLocation(workflow_dir)
            self._ui.graphicsView.setViewParameters(m.scene().getViewParameters())
            self._update_ui()
        except:
            self.close()
            raise

        om = self._mainWindow.model().optionsManager()
        om.setOption(PREVIOUS_WORKFLOW, workflow_dir)

    def close(self):
        self._mainWindow.confirm_close()
        m = self._mainWindow.model().workflowManager()
        self._undoStack.clear()
        self._graphicsScene.clear()
        m.close()
        self._update_ui()

    def save(self):
        m = self._mainWindow.model().workflowManager()
        location_set = os.path.exists(m.location())
        if location_set:
            self._updateLocation()
        else:
            location_set = self._setLocation()
        if location_set:
            m.scene().setViewParameters(self._ui.graphicsView.getViewParameters())
            m.save()
            if self.commitChanges(m.location()):
                self._setIndexerFile(m.location())
            else:
                pass  # undo changes

        self._update_ui()

    def saveAs(self):
        location_set = self._setLocation()
        if location_set:
            self.save()

    def _updateLocation(self):
        m = self._mainWindow.model().workflowManager()
        workflow_dir = m.location()
        if m.updateLocation(workflow_dir):
            self._ui.graphicsView.setLocation(workflow_dir)
            self._graphicsScene.updateModel()

    def _setLocation(self):
        location_set = False
        m = self._mainWindow.model().workflowManager()
        workflow_dir = self._getWorkflowDir()
        if workflow_dir:
            m.setPreviousLocation(workflow_dir)
            m.updateLocation(workflow_dir)
            self._ui.graphicsView.setLocation(workflow_dir)
            self._graphicsScene.updateModel()
            location_set = True

        return location_set

    def commitChanges(self, workflowDir):
        om = self._mainWindow.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
        if not pmr_tool.hasDVCS(workflowDir):
            # nothing to commit.
            return True

        return self._commitChanges(workflowDir, 'Workflow saved.')

    @handle_runtime_error
    @set_wait_cursor
    def _commitChanges(self, workflowDir, comment, commit_local=False):
        committed_changes = False
        om = self._mainWindow.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))
        try:
            workflow_files = [workflowDir + '/%s' % (DEFAULT_WORKFLOW_PROJECT_FILENAME),
                              workflowDir + '/%s' % (DEFAULT_WORKFLOW_ANNOTATION_FILENAME)]
            for f in os.listdir(workflowDir):
                if f.endswith(".conf"):
                    full_filename = os.path.join(workflowDir, f)
                    if full_filename not in workflow_files:
                        workflow_files.append(full_filename)

            pmr_tool.commitFiles(workflowDir, comment, workflow_files)
#                 [workflowDir + '/%s' % (DEFAULT_WORKFLOW_PROJECT_FILENAME),
#                  workflowDir + '/%s' % (DEFAULT_WORKFLOW_ANNOTATION_FILENAME)])  # XXX make/use file tracker
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
        om = self._mainWindow.model().optionsManager()
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info, use_external_git=om.getOption(USE_EXTERNAL_GIT))

        if not pmr_tool.hasDVCS(workflow_dir):
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
        self._ui.graphicsView.zoomIn()

    def zoom_out(self):
        self._ui.graphicsView.zoomOut()

    def _create_menu_items(self):
        menu_file = self._mainWindow.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_File')
        menu_workflow = self._mainWindow.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_Workflow')
        menu_view = self._mainWindow.get_menu_bar().findChild(QtWidgets.QMenu, 'menu_View')

        last_view_menu_action = menu_view.actions()[-1]
        last_file_menu_action = menu_file.actions()[-1]

        menu_new = QtWidgets.QMenu('&New', menu_file)
#        menu_Open = QtGui.QMenu('&Open', menu_File)

        self.action_NewPMR = QtWidgets.QAction('PMR Workflow', menu_new)
        self._set_action_properties(self.action_NewPMR, 'action_NewPMR', self.newpmr, 'Ctrl+N',
                                    'Create a new PMR based Workflow')
        self.action_New = QtWidgets.QAction('Workflow', menu_new)
        self._set_action_properties(self.action_New, 'action_New', self.new, 'Ctrl+Shift+N', 'Create a new Workflow')
        self.action_Open = QtWidgets.QAction('&Open', menu_file)
        self._set_action_properties(self.action_Open, 'action_Open', self.open, 'Ctrl+O', 'Open an existing Workflow')
        self.action_Import = QtWidgets.QAction('I&mport', menu_file)
        self._set_action_properties(self.action_Import, 'action_Import', self.importFromPMR, 'Ctrl+M',
                                    'Import existing Workflow from PMR')
        self.action_Update = QtWidgets.QAction('&Update', menu_file)
        self._set_action_properties(self.action_Update, 'action_Update', self.updateFromPMR, 'Ctrl+U',
                                    'update existing PMR Workflow')
        self.action_Close = QtWidgets.QAction('&Close', menu_file)
        self._set_action_properties(self.action_Close, 'action_Close', self.close, 'Ctrl+W', 'Close open Workflow')
        self.action_Save = QtWidgets.QAction('&Save', menu_file)
        self._set_action_properties(self.action_Save, 'action_Save', self.save, 'Ctrl+S', 'Save Workflow')
        self.action_SaveAs = QtWidgets.QAction('Save As', menu_file)
        self._set_action_properties(self.action_SaveAs, 'action_SaveAs', self.saveAs, '', 'Save Workflow as ...')
        self.action_Execute = QtWidgets.QAction('E&xecute', menu_workflow)
        self._set_action_properties(self.action_Execute, 'action_Execute', self.executeWorkflow, 'Ctrl+X',
                                    'Execute Workflow')
        self.action_Continue = QtWidgets.QAction('&Continue', menu_workflow)
        self._set_action_properties(self.action_Continue, 'action_Continue', self.continueWorkflow, 'Ctrl+T',
                                    'Continue executing Workflow')

        self.action_ZoomIn = QtWidgets.QAction('Zoom In', menu_view)
        self._set_action_properties(self.action_ZoomIn, 'action_ZoomIn', self.zoom_in, 'Ctrl++',
                                    'Zoom in Workflow')
        self.action_ZoomOut = QtWidgets.QAction('Zoom Out', menu_view)
        self._set_action_properties(self.action_ZoomOut, 'action_ZoomOut', self.zoom_out, 'Ctrl+-',
                                    'Zoom out Workflow')

        menu_new.insertAction(QtWidgets.QAction(self), self.action_NewPMR)
        menu_new.insertAction(QtWidgets.QAction(self), self.action_New)

        menu_file.insertMenu(last_file_menu_action, menu_new)
        menu_file.insertAction(last_file_menu_action, self.action_Open)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Save)
        menu_file.insertAction(last_file_menu_action, self.action_SaveAs)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Import)
        menu_file.insertAction(last_file_menu_action, self.action_Update)
        menu_file.insertSeparator(last_file_menu_action)
        menu_file.insertAction(last_file_menu_action, self.action_Close)
        menu_file.insertSeparator(last_file_menu_action)

        menu_view.addAction(self.action_ZoomIn)
        menu_view.addAction(self.action_ZoomOut)
        menu_view.insertSeparator(last_view_menu_action)

        menu_workflow.addAction(self.action_Execute)
        menu_workflow.addAction(self.action_Continue)
