'''
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
'''
import os, logging, subprocess, sys
from PySide import QtCore, QtGui

from requests.exceptions import HTTPError
from mapclient.exceptions import ClientRuntimeError

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, \
    DEFAULT_WORKFLOW_ANNOTATION_FILENAME

from mapclient.widgets.utils import set_wait_cursor
from mapclient.widgets.utils import handle_runtime_error

from mapclient.widgets.ui_workflowwidget import Ui_WorkflowWidget
from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclient.widgets.workflowgraphicsscene import WorkflowGraphicsScene
from mapclient.core import workflow
from mapclient.tools.pmr.pmrtool import PMRTool
# from mapclient.tools.pmr.pmrhgcommitdialog import PMRHgCommitDialog
from mapclient.widgets.importworkflowdialog import ImportWorkflowDialog
import shutil
from mapclient.application import initialiseLogLocation
from mapclient.tools.pluginupdater import PluginUpdater    
from mapclient.core.utils import convertExceptionToMessage

logger = logging.getLogger(__name__)


class WorkflowWidget(QtGui.QWidget):
    '''
    classdocs
    '''
    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent=mainWindow)
        self._mainWindow = mainWindow
        self._ui = Ui_WorkflowWidget()
        self._ui.setupUi(self)
        
        self._pluginUpdater = PluginUpdater()

        self._undoStack = QtGui.QUndoStack(self)
        self._undoStack.indexChanged.connect(self.undoStackIndexChanged)
        
        self._workflowManager = self._mainWindow.model().workflowManager()
        self._graphicsScene = WorkflowGraphicsScene(self)
        self._ui.graphicsView.setScene(self._graphicsScene)

        self._ui.graphicsView.setUndoStack(self._undoStack)
        self._graphicsScene.setUndoStack(self._undoStack)

        self._graphicsScene.setWorkflowScene(self._workflowManager.scene())
        self._graphicsScene.selectionChanged.connect(self._ui.graphicsView.selectionChanged)

        self._ui.executeButton.clicked.connect(self.executeWorkflow)
        self.action_Close = None  # Keep a handle to this for modifying the Ui.
        self._action_annotation = self._mainWindow.findChild(QtGui.QAction, "actionAnnotation")
        self._createMenuItems()

        self.updateStepTree()

        self._updateUi()

    def _updateUi(self):
        if hasattr(self, '_mainWindow'):
            try:
                wfm = self._mainWindow.model().workflowManager()
                self._mainWindow.setWindowTitle(wfm.title())
            except RuntimeError:
                return

            widget_visible = self.isVisible()

            workflow_open = wfm.isWorkflowOpen()
            self.action_Close.setEnabled(workflow_open and widget_visible)
            self.setEnabled(workflow_open and widget_visible)
            self.action_Save.setEnabled(wfm.isModified() and widget_visible)
            self._action_annotation.setEnabled(workflow_open and widget_visible)
            self.action_Import.setEnabled(widget_visible)
            self.action_New.setEnabled(widget_visible)
            self.action_NewPMR.setEnabled(widget_visible)
            self.action_Open.setEnabled(widget_visible)
            self.action_Execute.setEnabled(workflow_open and widget_visible)

    def updateStepTree(self):
        self._ui.stepTree.clear()
        for step in WorkflowStepMountPoint.getPlugins(''):
            self._ui.stepTree.addStep(step)

    def undoStackIndexChanged(self, index):
        self._mainWindow.model().workflowManager().undoStackIndexChanged(index)
        self._updateUi()

    def undoRedoStack(self):
        return self._undoStack

    def showEvent(self, *args, **kwargs):
        self._updateUi()
        return QtGui.QWidget.showEvent(self, *args, **kwargs)

    def hideEvent(self, *args, **kwargs):
        self._updateUi()
        return QtGui.QWidget.hideEvent(self, *args, **kwargs)

    def executeNext(self):
        self._mainWindow.execute()

    def executeWorkflow(self):
        wfm = self._mainWindow.model().workflowManager()
        errors = []

        if wfm.isModified():
            errors.append('The workflow has not been saved.')

        if not wfm.scene().canExecute():
            errors.append('Not all steps in the workflow have been '
                'successfully configured.')

        if not errors:
            self._mainWindow.execute()  # .model().workflowManager().execute()
        else:
            errors_str = '\n'.join(
                ['  %d. %s' % (i + 1, e) for i, e in enumerate(errors)])
            error_msg = ('The workflow could not be executed for the '
                'following reason%s:\n\n%s' % (
                    len(errors) > 1 and 's' or '', errors_str,
            ))
            QtGui.QMessageBox.critical(self, 'Workflow Execution', error_msg,
                QtGui.QMessageBox.Ok)

    def identifierOccursCount(self, identifier):
        return self._mainWindow.model().workflowManager().identifierOccursCount(identifier)

    def setCurrentWidget(self, widget):
        self._mainWindow.setCurrentWidget(widget)

    def setWidgetUndoRedoStack(self, stack):
        self._mainWindow.setCurrentUndoRedoStack(stack)

    def new(self, pmr=False):
        workflowDir = self._getWorkflowDir()
        if workflowDir:
            self._createNewWorkflow(workflowDir, pmr)

    def _getWorkflowDir(self):
        m = self._mainWindow.model().workflowManager()
        workflowDir = QtGui.QFileDialog.getExistingDirectory(self._mainWindow, caption='Select Workflow Directory', directory=m.previousLocation())
        if not workflowDir:
            # user abort
            return ''

        class ProblemClass(object):
            _mk_workflow_dir = False
            _rm_tree_success = True
            def rmTreeUnsuccessful(self, one, two, three):
                self._rm_tree_success = False

        if m.exists(workflowDir):
            # Check to make sure user wishes to overwrite existing workflow.
            ret = QtGui.QMessageBox.warning(self,
                'Replace Existing Workflow',
                'A Workflow already exists at this location.  '
                    'Do you want to replace this Workflow?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            # (QtGui.QMessageBox.Warning, '')
            if ret == QtGui.QMessageBox.No:
                # user abort
                return ''
            else:
                # Delete contents of directory
                shutil.rmtree(workflowDir, onerror=ProblemClass.rmTreeUnsuccessful)
                ProblemClass._mk_workflow_dir = True

        # got dir, continue
        if ProblemClass._rm_tree_success:
            if ProblemClass._mk_workflow_dir:
                os.mkdir(workflowDir)
            return workflowDir
        else:
            QtGui.QMessageBox.warning(self,
                'Replace Existing Workflow',
                'Could not remove existing workflow,'
                'New workflow not created.',
                QtGui.QMessageBox.Ok)

        return ''

    @handle_runtime_error
    @set_wait_cursor
    def _createNewWorkflow(self, workflowDir, pmr):
        m = self._mainWindow.model().workflowManager()
        m.new(workflowDir)
        m.setPreviousLocation(workflowDir)

        if pmr:
            pmr_info = PMR()
            pmr_tool = PMRTool(pmr_info)
            if pmr_tool.hasAccess():
                dir_name = os.path.basename(workflowDir)
                try:
                    repourl = pmr_tool.addWorkspace('Workflow: ' + dir_name, None)
                    pmr_tool.linkWorkspaceDirToUrl(workflowDir, repourl)
                except HTTPError as e:
                    logger.exception('Error creating new')
                    self.close()
                    raise ClientRuntimeError(
                        'Error Creating New', e.message)
            else:
                raise ClientRuntimeError('Error Creating New', "Client doesn't have access to PMR")

        self._undoStack.clear()
        self._ui.graphicsView.setLocation(workflowDir)
        self._graphicsScene.updateModel()
        self._updateUi()

    def newpmr(self):
        self.new(pmr=True)

    def load(self):
        m = self._mainWindow.model().workflowManager()
        # Warning: when switching between PySide and PyQt4 the keyword argument for the directory to initialise the dialog to is different.
        # In PySide the keyword argument is 'dir'
        # In PyQt4 the keyword argument is 'directory'
        workflowDir = QtGui.QFileDialog.getExistingDirectory(
            self._mainWindow,
            caption='Open Workflow',
            dir=m.previousLocation(),
            options=(
                QtGui.QFileDialog.ShowDirsOnly |
                QtGui.QFileDialog.DontResolveSymlinks |
                QtGui.QFileDialog.ReadOnly
            )
        )
        if len(workflowDir) > 0:
            self.performWorkflowChecks(workflowDir)
            try:
                m.load(workflowDir)
                m.setPreviousLocation(workflowDir)
                self._ui.graphicsView.setLocation(workflowDir)
                self._graphicsScene.updateModel()
                self._updateUi()
            except (ValueError, workflow.WorkflowError) as e:
                self.close()
                QtGui.QMessageBox.critical(self, 'Error Caught',
                    'Invalid Workflow.  ' + str(e))
                    
    def checkRequiredPlugins(self, wf):
        pluginDict = {}
        wf.beginGroup('required_plugins')
        pluginCount = wf.beginReadArray('plugin')
        for i in range(pluginCount):
            wf.setArrayIndex(i)
            pluginDict[wf.value('name')] = {
                'author':wf.value('author'),
                'version':wf.value('version'),
                'location':wf.value('location')
            }
        wf.endArray()
        wf.endGroup()
        
        required_plugins = {}
        locationManager = self._mainWindow.model().pluginManager().getPluginLocationManager()
        pluginDatabase = locationManager.getPluginDatabase()
        for plugin in pluginDict.keys():
            if not (plugin in pluginDatabase.keys() and \
                pluginDict[plugin]['author'] == pluginDatabase[plugin]['author'] and \
                pluginDict[plugin]['version'] == pluginDatabase[plugin]['version']):
                required_plugins[plugin] = pluginDict[plugin]
        return required_plugins
        
    def showDownloadableContent(self, plugins, dependencies):
        from mapclient.widgets.plugindownloader import PluginDownloader
        dlg = PluginDownloader()
        dlg.fillPluginTable(plugins)
        dlg.fillDependenciesTable(dependencies)
        dlg.setModal(True)
        if dlg.exec_():
            if dlg._downloadDependencies:
                self._mainWindow.model().pluginManager()._unsuccessful_package_installations = self.installPluginDependencies(dependencies)
            if dlg._downloadPlugins:
                directory = QtGui.QFileDialog.getExistingDirectory(caption='Select Plugin Directory', dir = '', options=QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
                if directory != '':
                    pm = self._mainWindow.model().pluginManager()
                    pluginDirs = pm.directories()
                    if directory not in pluginDirs:
                        pluginDirs.append(directory)
                        pm.setDirectories(pluginDirs)
                    self.downloadPlugins(plugins, directory)
            
    def downloadPlugins(self, plugins, directory):
        from mapclient.widgets.pluginprogress import PluginProgress
        self.dlg = PluginProgress(plugins, directory)
        self.dlg.show()        
        self.dlg.run()
        
    def checkRequiredDependencies(self, settings):
        self._workflowDependencies = {}
        settings.beginGroup('required_plugins')
        plugin_count = settings.beginReadArray('plugin')
        for i in range(plugin_count):
            settings.setArrayIndex(i)
            self._workflowDependencies[settings.value('name')] = settings.value('dependencies').split(' -- ')
        settings.endArray()
        settings.endGroup()
        return self._workflowDependencies
    
    def installPluginDependencies(self, plugin_dependencies):
        dependencies = []
        for plugin in plugin_dependencies:
            for dependency in plugin_dependencies[plugin]:
                if dependency not in dependencies:
                    dependencies += [dependency]
        unsuccessful_installs = self.pipInstallDependency(dependencies)
        return unsuccessful_installs        
        
    def pipInstallDependency(self, dependencies):
        from mapclient.widgets.dependency_installation import Install_Dependencies
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.installer = Install_Dependencies(dependencies, self.getVirtEnvLocation())
        self.installer.show()
        unsuccessful_installs = self.installer.run()
        self.installer.close()
        if unsuccessful_installs.keys():
           QtGui.QMessageBox.critical(self, 'Failed Installation', 'One or more of the required dependencies could not be installed.\nPlease refer to the program logs for more information.', QtGui.QMessageBox.Ok)
        return unsuccessful_installs
    
    def locateMAPClientVirtEnv(self, virtEnvDir):
        virtEnvDir = os.path.join(virtEnvDir, 'Scripts', 'activate.bat')
        return os.path.exists(virtEnvDir)
    
    def getVirtEnvLocation(self):
        virtEnvDir = initialiseLogLocation()[:-18]
        if virtEnvDir[-1] == '.':
            virtEnvDir = virtEnvDir + '.pluginVirtEnv'
        else:
            virtEnvDir = os.path.join(virtEnvDir[:-5], 'pluginVirtEnv')
        if not os.path.exists(virtEnvDir):
            os.makedirs(virtEnvDir)
        return virtEnvDir
        
    def setupMAPClientVirtEnv(self, env_dir):
        from mapclient.widgets.dependency_installation import VESetup
        self.dlg = VESetup(env_dir)
        self.dlg.setModal(True)
        self.dlg.show()
        self.dlg.run()
        self.dlg.exec()
        return self.locateMAPClientVirtEnv(self.getVirtEnvLocation())
        
    def compareRequirements(self, required_installs, dependencies):
        pythonExe = self.getVirtEnvLocation() + '\Scripts' + '\python.exe'
        pipExe = self.getVirtEnvLocation() + '\Scripts' + '\pip.exe'
        install_list_system = subprocess.check_output(['pip', 'list'])
        install_list_system = install_list_system.decode('utf-8')
        install_list_virtEnv = subprocess.check_output([pythonExe, pipExe, 'list'], shell=True)
        install_list_virtEnv = install_list_virtEnv.decode('utf-8')
        for dependency in dependencies.items():
            if dependency[-1][-1] != 'None':
                required_installs[dependency[0]] = []
                for requirement in dependency[-1]:
                    if requirement not in install_list_system and requirement not in install_list_virtEnv:
                            required_installs[dependency[0]] += [requirement]
        return required_installs
        
    def setupVEQuery(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('Application Virtual Environment')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setText('In order to install plugin dependencies a virtual environment\nneeds to be set up for MAP Client.\n\nWould you like to set it up now?')
        msgBox.setIcon(QtGui.QMessageBox.Question)
        yesButton = msgBox.addButton('Yes', QtGui.QMessageBox.AcceptRole)
        noButton = msgBox.addButton('No', QtGui.QMessageBox.RejectRole)
        msgBox.exec()
        
        if msgBox.clickedButton() == yesButton:
            return True
        elif msgBox.clickedButton() == noButton:
            return False
        
    def checkMissingDependencies(self, dependencies):
        virtEnvExec = self.locateMAPClientVirtEnv(self.getVirtEnvLocation())
        required_installs = {}
        if not virtEnvExec:
            if self.setupVEQuery():
                if self.setupMAPClientVirtEnv(self.getVirtEnvLocation()):
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                    required_installs = self.compareRequirements(required_installs, dependencies)
        else:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            required_installs = self.compareRequirements(required_installs, dependencies)
        return required_installs

    def performWorkflowChecks(self, workflowDir):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        wf = workflow._getWorkflowConfiguration(workflowDir)
        plugin_dependencies = self.checkRequiredDependencies(wf)
        dependencies = {}
        for info in plugin_dependencies.items():
            if info[-1] != 'None':
                dependencies[info[0]] = info[-1]
        QtGui.QApplication.restoreOverrideCursor()
        dependencies_to_install = self.checkMissingDependencies(dependencies)
        plugins = self.checkRequiredPlugins(wf)
        if plugins or dependencies_to_install:
            QtGui.QApplication.restoreOverrideCursor()
            self.showDownloadableContent(plugins, dependencies_to_install)
        
        pm = self._mainWindow.model().pluginManager()
        pm.load()
        self._mainWindow.showPluginErrors()
        self.updateStepTree()
        
    def importFromPMR(self):
        m = self._mainWindow.model().workflowManager()
        dlg = ImportWorkflowDialog(m.previousLocation(), self._mainWindow)
        if dlg.exec_():
            destination_dir = dlg.destinationDir()
            workspace_url = dlg.workspaceUrl()
            if os.path.exists(destination_dir) and workspace_url:
                try:
                    self._importFromPMR(workspace_url, destination_dir)
                except (ValueError, workflow.WorkflowError) as e:
                    QtGui.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + str(e))
            else:
                QtGui.QMessageBox.critical(self, 'Error Caught', 'Invalid Import Settings.  Either the workspace url (%s) was not set' \
                                           ' or the destination directory (%s) does not exist. ' % (workspace_url, destination_dir))

    @handle_runtime_error
    @set_wait_cursor
    def _importFromPMR(self, workspace_url, workflowDir):
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info)

        pmr_tool.cloneWorkspace(
            remote_workspace_url=workspace_url,
            local_workspace_dir=workflowDir,
        )
        
        self.performWorkflowChecks(workflowDir)
        logger.info('Analyze first before attempting load ...')
        try:
            m = self._mainWindow.model().workflowManager()
            m.load(workflowDir)
            m.setPreviousLocation(workflowDir)
            self._graphicsScene.updateModel()
            self._updateUi()
        except:
            self.close()
            raise

    def close(self):
        self._mainWindow.confirmClose()
        m = self._mainWindow.model().workflowManager()
        self._undoStack.clear()
        self._graphicsScene.clear()
        m.close()
        self._updateUi()

    def save(self):
        m = self._mainWindow.model().workflowManager()
        if not os.path.exists(m.location()):
            workflow_dir = self._getWorkflowDir()
            if workflow_dir:
                m.setPreviousLocation(workflow_dir)
                m.setLocation(workflow_dir)
        if m.location():
            m.save()
            if self.commitChanges(m.location()):
                self._setIndexerFile(m.location())
            else:
                pass  # undo changes

        self._updateUi()

    def commitChanges(self, workflowDir):
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info)
        if not pmr_tool.hasDVCS(workflowDir):
            # nothing to commit.
            return True

#         dlg = PMRHgCommitDialog(self)
#         dlg.setModal(True)
#         if dlg.exec_() == QtGui.QDialog.Rejected:
#             return False

#         action = dlg.action()
#         if action == QtGui.QDialogButtonBox.Ok:
#             return True
#         elif action == QtGui.QDialogButtonBox.Save:
#             return self._commitChanges(workflowDir, dlg.comment(), commit_local=True)

        return self._commitChanges(workflowDir, 'Generic comment for saving workflow.')

    @handle_runtime_error
    @set_wait_cursor
    def _commitChanges(self, workflowDir, comment, commit_local=False):
        committed_changes = False
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info)
        try:
            workflow_files = [workflowDir + '/%s' % (DEFAULT_WORKFLOW_PROJECT_FILENAME),
                              workflowDir + '/%s' % (DEFAULT_WORKFLOW_ANNOTATION_FILENAME)]
            for f in os.listdir(workflowDir):
                if f.endswith(".conf"):
                    full_filename = os.path.join(workflowDir, f)
                    if full_filename not in workflow_files:
                        workflow_files.append(full_filename)
                    
            print(workflow_files)
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
        pmr_info = PMR()
        pmr_tool = PMRTool(pmr_info)

        if not pmr_tool.hasDVCS(workflow_dir):
            return
        try:
            pmr_tool.addFileToIndexer(workflow_dir, DEFAULT_WORKFLOW_ANNOTATION_FILENAME)
#             pmr_tool.commitFiles(local_workspace_dir, message, files)
        except ClientRuntimeError:
            # handler will deal with this.
            raise

    def _setActionProperties(self, action, name, slot, shortcut='', statustip=''):
        action.setObjectName(name)
        action.triggered.connect(slot)
        if len(shortcut) > 0:
            action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setStatusTip(statustip)

    def _createMenuItems(self):
        menu_File = self._mainWindow.menubar.findChild(QtGui.QMenu, 'menu_File')
        menu_Project = self._mainWindow.menubar.findChild(QtGui.QMenu, 'menu_Project')

        lastFileMenuAction = menu_File.actions()[-1]
        menu_New = QtGui.QMenu('&New', menu_File)
#        menu_Open = QtGui.QMenu('&Open', menu_File)

        self.action_NewPMR = QtGui.QAction('PMR Workflow', menu_New)
        self._setActionProperties(self.action_NewPMR, 'action_NewPMR', self.newpmr, 'Ctrl+N', 'Create a new PMR based Workflow')
        self.action_New = QtGui.QAction('Workflow', menu_New)
        self._setActionProperties(self.action_New, 'action_New', self.new, 'Ctrl+Shift+N', 'Create a new Workflow')
        self.action_Open = QtGui.QAction('&Open', menu_File)
        self._setActionProperties(self.action_Open, 'action_Open', self.load, 'Ctrl+O', 'Open an existing Workflow')
        self.action_Import = QtGui.QAction('I&mport', menu_File)
        self._setActionProperties(self.action_Import, 'action_Import', self.importFromPMR, 'Ctrl+M', 'Import existing Workflow from PMR')
        self.action_Close = QtGui.QAction('&Close', menu_File)
        self._setActionProperties(self.action_Close, 'action_Close', self.close, 'Ctrl+W', 'Close open Workflow')
        self.action_Save = QtGui.QAction('&Save', menu_File)
        self._setActionProperties(self.action_Save, 'action_Save', self.save, 'Ctrl+S', 'Save Workflow')
        self.action_Execute = QtGui.QAction('E&xecute', menu_Project)
        self._setActionProperties(self.action_Execute, 'action_Execute', self.executeWorkflow, 'Ctrl+X', 'Execute Workflow')

        menu_New.insertAction(QtGui.QAction(self), self.action_NewPMR)
        menu_New.insertAction(QtGui.QAction(self), self.action_New)
        menu_File.insertMenu(lastFileMenuAction, menu_New)
        menu_File.insertAction(lastFileMenuAction, self.action_Open)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Import)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Close)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Save)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_Project.addAction(self.action_Execute)


