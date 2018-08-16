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

import logging
from PySide import QtGui

from mapclient.settings.general import getVirtualEnvSitePackagesDirectory
from mapclient.view.ui.ui_mainwindow import Ui_MainWindow
from mapclient.view.workflow.workflowwidget import WorkflowWidget
from mapclient.settings.info import DEFAULT_WORKFLOW_ANNOTATION_FILENAME
from mapclient.settings.definitions import VIRTUAL_ENV_PATH, WIZARD_TOOL_STRING, \
    VIRTUAL_ENVIRONMENT_STRING, PMR_TOOL_STRING, PYSIDE_RCC_EXE, \
    PREVIOUS_PW_WRITE_STEP_LOCATION, PREVIOUS_PW_ICON_LOCATION, USE_EXTERNAL_GIT
from mapclient.view.utils import set_wait_cursor

logger = logging.getLogger(__name__)

ADMIN_MODE = False


class MainWindow(QtGui.QMainWindow):
    """
    This is the main window for the MAP Client.
    """

    def __init__(self, model):
        QtGui.QMainWindow.__init__(self)
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._setupMenus()
        self.setMenuBar(self.menubar)
        self._makeConnections()

        self.action_Annotation.setEnabled(False)

        self._createUndoAction(self.menu_Edit)
        self._createRedoAction(self.menu_Edit)

        self._model.readSettings()
        self.resize(self._model.size())
        self.move(self._model.pos())

        self._workflowWidget = WorkflowWidget(self)
        self._ui.stackedWidget.addWidget(self._workflowWidget)
        self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())

        self._model.workflowManager().scene().setMainWindow(self)
        self._pluginManagerDlg = None

    def _setupMenus(self):
        """
        Because of OS X we have to setup the menubar with no parent so we do
        it manually here instead of through designer.
        """
        self.menubar = QtGui.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Workflow = QtGui.QMenu(self.menubar)
        self.menu_Workflow.setObjectName("menu_Workflow")
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
        self.action_LogInformation = QtGui.QAction(self)
        self.action_LogInformation.setObjectName("action_LogInformation")
        self.action_Options = QtGui.QAction(self)
        self.action_Options.setObjectName("action_Options")
        self.action_About = QtGui.QAction(self)
        self.action_About.setObjectName("action_About")
        self.action_Quit = QtGui.QAction(self)
        self.action_Quit.setObjectName("action_Quit")
        self.action_PluginManager = QtGui.QAction(self)
        self.action_PluginManager.setObjectName("action_PluginManager")
        self.action_PMR = QtGui.QAction(self)
        self.action_PMR.setObjectName("action_PMR")
        self.action_RenamePlugin = QtGui.QAction(self)
        self.action_RenamePlugin.setObjectName("action_RenamePlugin")
        self.action_Annotation = QtGui.QAction(self)
        self.action_Annotation.setObjectName("action_Annotation")
        self.action_PluginWizard = QtGui.QAction(self)
        self.action_PluginWizard.setObjectName("action_PluginWizard")
        if ADMIN_MODE:
            self.action_MAPIcon = QtGui.QAction(self)
            self.action_MAPIcon.setObjectName("actionMAPIcon")

        self.menu_Help.addAction(self.action_About)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_LogInformation)
        self.menu_View.addAction(self.action_Options)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Tools.addAction(self.action_PluginManager)
        self.menu_Tools.addAction(self.action_PluginWizard)
        self.menu_Tools.addAction(self.action_PMR)
        self.menu_Tools.addAction(self.action_RenamePlugin)
        self.menu_Tools.addAction(self.action_Annotation)
        if ADMIN_MODE:
            self.menu_Tools.addAction(self.action_MAPIcon)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Workflow.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self._retranslateUi()

    def _retranslateUi(self):
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Workflow.setTitle(QtGui.QApplication.translate("MainWindow", "&Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Quit the application", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_LogInformation.setText(QtGui.QApplication.translate("MainWindow", "Log Information", None, QtGui.QApplication.UnicodeUTF8))
        self.action_LogInformation.setStatusTip(QtGui.QApplication.translate("MainWindow", "Inspect logged program information", None, QtGui.QApplication.UnicodeUTF8))
        self.action_LogInformation.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Options.setText(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Options.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change global application options", None, QtGui.QApplication.UnicodeUTF8))
        self.action_PluginManager.setText(QtGui.QApplication.translate("MainWindow", "Plugin &Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.action_PMR.setText(QtGui.QApplication.translate("MainWindow", "&PMR", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Annotation.setText(QtGui.QApplication.translate("MainWindow", "&Annotation", None, QtGui.QApplication.UnicodeUTF8))
        self.action_PluginWizard.setText(QtGui.QApplication.translate("MainWindow", "Plugin Wi&zard", None, QtGui.QApplication.UnicodeUTF8))
        self.action_RenamePlugin.setText(QtGui.QApplication.translate("MainWindow", "&Rename Plugin", None, QtGui.QApplication.UnicodeUTF8))
        if ADMIN_MODE:
            self.action_MAPIcon.setText(QtGui.QApplication.translate("MainWindow", "MAP &Icon", None, QtGui.QApplication.UnicodeUTF8))

    def _createUndoAction(self, parent):
        self.undoAction = QtGui.QAction('Undo', parent)
        self.undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        self.undoAction.triggered.connect(self._model.undoManager().undo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.undoAction.setEnabled(stack.canUndo())
        else:
            self.undoAction.setEnabled(False)

        parent.addAction(self.undoAction)

    def _createRedoAction(self, parent):
        self.redoAction = QtGui.QAction('Redo', parent)
        self.redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))
        self.redoAction.triggered.connect(self._model.undoManager().redo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.redoAction.setEnabled(stack.canRedo())
        else:
            self.redoAction.setEnabled(False)

        parent.addAction(self.redoAction)

    def model(self):
        return self._model

    def _makeConnections(self):
        self.action_Quit.triggered.connect(self.quitApplication)
        self.action_About.triggered.connect(self.about)
        self.action_LogInformation.triggered.connect(self.showLogInformationDialog)
        self.action_Options.triggered.connect(self.showOptionsDialog)
        self.action_PluginManager.triggered.connect(self.showPluginManagerDialog)
        self.action_PluginWizard.triggered.connect(self.showPluginWizardDialog)
        self.action_PMR.triggered.connect(self.showPMRTool)
        self.action_Annotation.triggered.connect(self.showAnnotationTool)
        self.action_RenamePlugin.triggered.connect(self.showRenamePluginDialog)
        if ADMIN_MODE:
            self.action_MAPIcon.triggered.connect(self.showMAPIconDialog)

    def checkApplicationSetup(self):
        """
        Check the application setup and return True if the application
        has been setup or the checks are not required, False otherwise.
        :return: True if setup is ok or not required, False otherwise.
        """
        return self._model.doEnvironmentChecks()

    def setupApplication(self):
        """
        Setup the application, check for git, and pyside-rcc.
        """
        pass

    def loadPlugins(self):
        pm = self._model.pluginManager()

        self._pluginManagerLoadPlugins()
        # Show plugin errors
        if pm.haveErrors():
            self.showPluginErrorsDialog()

    def openWorkflow(self, workflowDir):
        self._workflowWidget.openWorkflow(workflowDir)

    def setCurrentUndoRedoStack(self, stack):
        current_stack = self._model.undoManager().currentStack()
        if current_stack:
            current_stack.canRedoChanged.disconnect(self._canRedoChanged)
            current_stack.canUndoChanged.disconnect(self._canUndoChanged)

        self._model.undoManager().setCurrentStack(stack)

        self.redoAction.setEnabled(stack.canRedo())
        self.undoAction.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._canUndoChanged)
        stack.canRedoChanged.connect(self._canRedoChanged)

    def _canRedoChanged(self, canRedo):
        self.redoAction.setEnabled(canRedo)

    def _canUndoChanged(self, canUndo):
        self.undoAction.setEnabled(canUndo)

    def execute(self):
        if self._ui.stackedWidget.currentWidget() != self._workflowWidget:
            self._ui.stackedWidget.setCurrentWidget(self._workflowWidget)
            self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())
        self.model().workflowManager().execute()

    @set_wait_cursor
    def setCurrentWidget(self, widget):
        if self._ui.stackedWidget.indexOf(widget) <= 0:
            self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def currentWidget(self):
        return self._ui.stackedWidget.currentWidget()

    def closeEvent(self, event):
        self.quitApplication()

    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.workflowManager().isModified():
            ret = QtGui.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self._model.workflowManager().save()

    def quitApplication(self):
        self.confirmClose()

        self._model.setSize(self.size())
        self._model.setPos(self.pos())
        self._model.writeSettings()
        QtGui.qApp.quit()

    def about(self):
        from mapclient.view.dialogs.about.aboutdialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def showLogInformationDialog(self):
        from mapclient.view.dialogs.log.loginformation import LogInformation
        dlg = LogInformation(self)
        dlg.fillTable(self)
        dlg.setModal(True)
        dlg.exec_()

    def showOptionsDialog(self, current_tab=0):
        from mapclient.view.managers.options.optionsdialog import OptionsDialog

        om = self._model.optionsManager()
        options = om.getOptions()
        dlg = OptionsDialog(self)
        dlg.setCurrentTab(current_tab)
        dlg.load(options)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            if dlg.isModified():
                om.setOptions(dlg.save())

        # set availability of functionality.
        pm = self._model.pluginManager()
        self.action_PluginWizard.setEnabled(dlg.checkedOk(WIZARD_TOOL_STRING))
        self.action_PMR.setEnabled(dlg.checkedOk(PMR_TOOL_STRING))
        self._workflowWidget.applyOptions()

    def showPluginManagerDialog(self):
        from mapclient.view.managers.plugins.pluginmanagerdialog import PluginManagerDialog
        pm = self._model.pluginManager()
#         pluginErrors = pm.getPluginErrors()
#         print(pluginErrors)
        dlg = PluginManagerDialog(self._model.pluginManager()._ignoredPlugins, self._model.pluginManager()._doNotShowPluginErrors, self._model.pluginManager()._resourceFiles, self._model.pluginManager()._updaterSettings, self._model.pluginManager()._unsuccessful_package_installations, self)
        self._pluginManagerDlg = dlg
        dlg.setDirectories(pm.directories())
        dlg.setLoadDefaultPlugins(pm.loadDefaultPlugins())
        dlg.reloadPlugins = self._pluginManagerLoadPlugins

        dlg.setModal(True)
        if dlg.exec_():
            pm._ignoredPlugins = dlg._ignoredPlugins
            pm._doNotShowPluginErrors = dlg._do_not_show_plugin_errors
            pm._resourceFiles = dlg._resource_filenames
            pm._updaterSettings = dlg._updaterSettings
            self._pluginManagerLoadPlugins()

        self._pluginManagerDlg = None

    @set_wait_cursor
    def _pluginManagerLoadPlugins(self):
        """
        Get the plugin manager to load the current plugins.
        """
        pm = self._model.pluginManager()
        # Are we currently using the plugin manager dialog?
        if self._pluginManagerDlg is not None:
            pm.setReloadPlugins()
            pm.setDirectories(self._pluginManagerDlg.directories())
            pm.setLoadDefaultPlugins(self._pluginManagerDlg.loadDefaultPlugins())

        if pm.reloadPlugins():
            pm.load()
            wm = self._model.workflowManager()
            wm.updateAvailableSteps()
            self._workflowWidget.updateStepTree()

#             self.showPluginErrors()

    def showPluginWizardDialog(self):
        from mapclient.tools.pluginwizard.wizarddialog import WizardDialog
        from mapclient.tools.pluginwizard.skeleton import Skeleton

        om = self._model.optionsManager()

        dlg = WizardDialog(self)
        dlg.setPreviousWriteStepLocation(om.getOption(PREVIOUS_PW_WRITE_STEP_LOCATION))
        dlg.setPreviousIconLocation(om.getOption(PREVIOUS_PW_ICON_LOCATION))

        dlg.setModal(True)
        if dlg.exec_() == dlg.Accepted:
            om.setOption(PREVIOUS_PW_WRITE_STEP_LOCATION, dlg.getPreviousWriteStepLocation())
            om.setOption(PREVIOUS_PW_ICON_LOCATION, dlg.getPreviousIconLocation())

            s = Skeleton(dlg.getOptions(), om.getOption(PYSIDE_RCC_EXE))
            try:
                s.write()
                pm = self._model.pluginManager()
                pm.setReloadPlugins()
                self._pluginManagerLoadPlugins()
                QtGui.QMessageBox.information(self, 'Skeleton Step', 'The Skeleton step has successfully been written to disk.')
            except Exception as e:
                QtGui.QMessageBox.critical(self, 'Error Writing Step', 'There was an error writing the step, perhaps the step already exists?')
                logger.critical(e)
                import os
                package_directory = s.getPackageDirectory()
                if os.path.exists(package_directory):
                    logger.info('Removing partially created skeleton step "{0}"'.format(package_directory))
                    import shutil
                    shutil.rmtree(package_directory)

    def showRenamePluginDialog(self):
        from mapclient.tools.renameplugin.renamedialog import RenameDialog

        om = self._model.optionsManager()
        dlg = RenameDialog(om.getOption(PYSIDE_RCC_EXE), self)
        dlg.setModal(True)
        dlg.exec_()

    def showPMRTool(self):
        om = self._model.optionsManager()
        from mapclient.tools.pmr.dialogs.register import PMRRegisterDialog
        dlg = PMRRegisterDialog(om.getOption(USE_EXTERNAL_GIT), self)
        dlg.setModal(True)
        dlg.exec_()

    def showAnnotationTool(self):
        from mapclient.tools.annotation.annotationdialog import AnnotationDialog
        location = self._model.workflowManager().location()
        dlg = AnnotationDialog(location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, self)
        dlg.setModal(True)
        dlg.exec_()

    def showMAPIconDialog(self):
        from mapclient.tools.mapicon.mapicondialog import MAPIconDialog
        location = self._model.workflowManager().location()
        dlg = MAPIconDialog(location, self)
        dlg.setModal(True)
        if dlg.exec_():
            dlg.createIcon()

    def showPluginErrorsDialog(self):
        from mapclient.view.managers.plugins.pluginerrors import PluginErrors

        pm = self._model.pluginManager()
        if pm.haveErrors():
            return
            dlg = PluginErrors(pm.getPluginErrors(), pm.getIgnoredPlugins(), pm.getResourceFiles(), pm.getUpdaterSettings())
            if not self._doNotShowPluginErrors:
                dlg.setModal(True)
                dlg.fillList()
                dlg.exec_()
            ignored_plugins = dlg.getIgnoredPlugins()
            for plugin in ignored_plugins:
                if plugin not in self._ignoredPlugins:
                    self._ignoredPlugins += [plugin]
            if dlg._doNotShow:
                self._doNotShowPluginErrors = True
            if dlg._hotfixExecuted:
                self.load()


