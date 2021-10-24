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

from PySide2 import QtWidgets, QtGui

from mapclient.view.ui.ui_mainwindow import Ui_MainWindow
from mapclient.view.workflow.workflowwidget import WorkflowWidget
from mapclient.settings.info import DEFAULT_WORKFLOW_ANNOTATION_FILENAME
from mapclient.settings.definitions import WIZARD_TOOL_STRING, \
    PMR_TOOL_STRING, PYSIDE_RCC_EXE, USE_EXTERNAL_RCC, PYSIDE_UIC_EXE, USE_EXTERNAL_UIC, \
    PREVIOUS_PW_WRITE_STEP_LOCATION, PREVIOUS_PW_ICON_LOCATION, USE_EXTERNAL_GIT
from mapclient.view.utils import set_wait_cursor

logger = logging.getLogger(__name__)

ADMIN_MODE = False


class MainWindow(QtWidgets.QMainWindow):
    """
    This is the main window for the MAP Client.
    """

    def __init__(self, model):
        QtWidgets.QMainWindow.__init__(self)
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._setup_menus()
        self.setMenuBar(self._menu_bar)
        self._make_connections()

        self._action_Annotation.setEnabled(False)

        self._create_undo_action(self._menu_Edit)
        self._create_redo_action(self._menu_Edit)

        self._model.readSettings()

        self._workflowWidget = WorkflowWidget(self)
        self._ui.stackedWidget.addWidget(self._workflowWidget)
        self.set_current_undo_redo_stack(self._workflowWidget.undoRedoStack())

        self._model.workflowManager().scene().setMainWindow(self)
        self._pluginManagerDlg = None

    def showEvent(self, event):
        self.resize(self._model.size())
        self.move(self._model.pos())

    def _setup_menus(self):
        """
        Because of OS X we have to setup the menubar with no parent so we do
        it manually here instead of through designer.
        """
        self._menu_bar = QtWidgets.QMenuBar()
        self._menu_bar.setObjectName("menubar")
        self._menu_Help = QtWidgets.QMenu(self._menu_bar)
        self._menu_Help.setObjectName("menu_Help")
        self._menu_View = QtWidgets.QMenu(self._menu_bar)
        self._menu_View.setObjectName("menu_View")
        self._menu_File = QtWidgets.QMenu(self._menu_bar)
        self._menu_File.setObjectName("menu_File")
        self._menu_Edit = QtWidgets.QMenu(self._menu_bar)
        self._menu_Edit.setObjectName("menu_Edit")
        self._menu_Workflow = QtWidgets.QMenu(self._menu_bar)
        self._menu_Workflow.setObjectName("menu_Workflow")
        self._menu_Tools = QtWidgets.QMenu(self._menu_bar)
        self._menu_Tools.setObjectName("menu_Tools")
        self._action_LogInformation = QtWidgets.QAction(self)
        self._action_LogInformation.setObjectName("action_LogInformation")
        self._action_Options = QtWidgets.QAction(self)
        self._action_Options.setObjectName("action_Options")
        self._action_About = QtWidgets.QAction(self)
        self._action_About.setObjectName("action_About")
        self._action_Quit = QtWidgets.QAction(self)
        self._action_Quit.setObjectName("action_Quit")
        self._action_PluginManager = QtWidgets.QAction(self)
        self._action_PluginManager.setObjectName("action_PluginManager")
        self._action_PackageManager = QtWidgets.QAction(self)
        self._action_PackageManager.setObjectName("action_PackageManager")
        self._action_PMR = QtWidgets.QAction(self)
        self._action_PMR.setObjectName("action_PMR")
        self._action_RenamePlugin = QtWidgets.QAction(self)
        self._action_RenamePlugin.setObjectName("action_RenamePlugin")
        self._action_UpdateWorkflow = QtWidgets.QAction(self)
        self._action_UpdateWorkflow.setObjectName("action_UpdateWorkflow")
        self._action_Annotation = QtWidgets.QAction(self)
        self._action_Annotation.setObjectName("action_Annotation")
        self._action_PluginWizard = QtWidgets.QAction(self)
        self._action_PluginWizard.setObjectName("action_PluginWizard")
        if ADMIN_MODE:
            self._action_MAPIcon = QtWidgets.QAction(self)
            self._action_MAPIcon.setObjectName("actionMAPIcon")

        self._menu_Help.addAction(self._action_About)
        self._menu_View.addSeparator()
        self._menu_View.addAction(self._action_LogInformation)
        self._menu_View.addAction(self._action_Options)
        self._menu_File.addSeparator()
        self._menu_File.addAction(self._action_Quit)
        self._menu_Tools.addAction(self._action_PluginManager)
        self._menu_Tools.addAction(self._action_PackageManager)
        self._menu_Tools.addAction(self._action_PluginWizard)
        self._menu_Tools.addAction(self._action_PMR)
        self._menu_Tools.addAction(self._action_RenamePlugin)
        self._menu_Tools.addAction(self._action_UpdateWorkflow)
        self._menu_Tools.addAction(self._action_Annotation)
        if ADMIN_MODE:
            self._menu_Tools.addAction(self._action_MAPIcon)
        self._menu_bar.addAction(self._menu_File.menuAction())
        self._menu_bar.addAction(self._menu_Edit.menuAction())
        self._menu_bar.addAction(self._menu_View.menuAction())
        self._menu_bar.addAction(self._menu_Workflow.menuAction())
        self._menu_bar.addAction(self._menu_Tools.menuAction())
        self._menu_bar.addAction(self._menu_Help.menuAction())

        self._re_translate_ui()

    def _re_translate_ui(self):
        self._menu_Help.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Help", None, -1))
        self._menu_View.setTitle(QtWidgets.QApplication.translate("MainWindow", "&View", None, -1))
        self._menu_File.setTitle(QtWidgets.QApplication.translate("MainWindow", "&File", None, -1))
        self._menu_Edit.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Edit", None, -1))
        self._menu_Workflow.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Workflow", None, -1))
        self._menu_Tools.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Tools", None, -1))
        self._action_About.setText(QtWidgets.QApplication.translate("MainWindow", "&About", None, -1))
        self._action_Quit.setText(QtWidgets.QApplication.translate("MainWindow", "&Quit", None, -1))
        self._action_Quit.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Quit the application", None, -1))
        self._action_Quit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Q", None, -1))
        self._action_LogInformation.setText(QtWidgets.QApplication.translate("MainWindow", "Log Information", None, -1))
        self._action_LogInformation.setStatusTip(QtWidgets.QApplication.translate("MainWindow",
                                                                                  "Inspect logged program information",
                                                                                  None, -1))
        self._action_LogInformation.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+I", None, -1))
        self._action_Options.setText(QtWidgets.QApplication.translate("MainWindow", "Options", None, -1))
        self._action_Options.setStatusTip(QtWidgets.QApplication.translate("MainWindow",
                                                                           "Change global application options",
                                                                           None, -1))
        self._action_PluginManager.setText(QtWidgets.QApplication.translate("MainWindow", "Plugin &Manager", None, -1))
        self._action_PackageManager.setText(QtWidgets.QApplication.translate("MainWindow", "Package Ma&nager", None, -1))
        self._action_PMR.setText(QtWidgets.QApplication.translate("MainWindow", "&PMR", None, -1))
        self._action_Annotation.setText(QtWidgets.QApplication.translate("MainWindow", "&Annotation", None, -1))
        self._action_PluginWizard.setText(QtWidgets.QApplication.translate("MainWindow", "Plugin Wi&zard", None, -1))
        self._action_RenamePlugin.setText(QtWidgets.QApplication.translate("MainWindow", "&Rename Plugin", None, -1))
        self._action_UpdateWorkflow.setText(QtWidgets.QApplication.translate("MainWindow", "&Update Workflow", None, -1))
        if ADMIN_MODE:
            self._action_MAPIcon.setText(QtWidgets.QApplication.translate("MainWindow", "MAP &Icon", None, -1))

    def _create_undo_action(self, parent):
        self._action_Undo = QtWidgets.QAction('Undo', parent)
        self._action_Undo.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        self._action_Undo.triggered.connect(self._model.undoManager().undo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self._action_Undo.setEnabled(stack.canUndo())
        else:
            self._action_Undo.setEnabled(False)

        parent.addAction(self._action_Undo)

    def _create_redo_action(self, parent):
        self._action_Redo = QtWidgets.QAction('Redo', parent)
        self._action_Redo.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))
        self._action_Redo.triggered.connect(self._model.undoManager().redo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self._action_Redo.setEnabled(stack.canRedo())
        else:
            self._action_Redo.setEnabled(False)

        parent.addAction(self._action_Redo)

    def model(self):
        return self._model

    def _make_connections(self):
        self._action_Quit.triggered.connect(self.quit_application)
        self._action_About.triggered.connect(self.about)
        self._action_LogInformation.triggered.connect(self._show_log_information_dialog)
        self._action_Options.triggered.connect(self.show_options_dialog)
        self._action_PluginManager.triggered.connect(self._show_plugin_manager_dialog)
        self._action_PackageManager.triggered.connect(self._show_package_manager_dialog)
        self._action_PluginWizard.triggered.connect(self._show_plugin_wizard_dialog)
        self._action_PMR.triggered.connect(self._show_pmr_tool)
        self._action_Annotation.triggered.connect(self._show_annotation_tool)
        self._action_RenamePlugin.triggered.connect(self._show_rename_plugin_dialog)
        self._action_UpdateWorkflow.triggered.connect(self._show_update_workflow_dialog)
        if ADMIN_MODE:
            self._action_MAPIcon.triggered.connect(self._show_map_icon_dialog)

    def check_application_setup(self):
        """
        Check the application setup and return True if the application
        has been setup or the checks are not required, False otherwise.
        :return: True if setup is ok or not required, False otherwise.
        """
        return self._model.doEnvironmentChecks()

    @staticmethod
    def setup_application():
        return False

    def get_menu_bar(self):
        return self._menu_bar

    def load_packages(self):
        pm = self._model.package_manager()
        pm.load()

    def load_plugins(self):
        pm = self._model.pluginManager()

        self._plugin_manager_load_plugins()
        # Show plugin errors
        if pm.haveErrors():
            self._show_plugin_errors_dialog()

    def open_workflow(self, workflowDir):
        self._workflowWidget.openWorkflow(workflowDir)

    def set_current_undo_redo_stack(self, stack):
        current_stack = self._model.undoManager().currentStack()
        if current_stack:
            current_stack.canRedoChanged.disconnect(self._can_redo_changed)
            current_stack.canUndoChanged.disconnect(self._can_undo_changed)

        self._model.undoManager().setCurrentStack(stack)

        self._action_Redo.setEnabled(stack.canRedo())
        self._action_Undo.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._can_undo_changed)
        stack.canRedoChanged.connect(self._can_redo_changed)

    def _can_redo_changed(self, canRedo):
        self._action_Redo.setEnabled(canRedo)

    def _can_undo_changed(self, canUndo):
        self._action_Undo.setEnabled(canUndo)

    def execute(self):
        if self.current_widget() != self._workflowWidget:
            self.set_current_widget(self._workflowWidget)
            self.set_current_undo_redo_stack(self._workflowWidget.undoRedoStack())
        self.model().workflowManager().execute()

    @set_wait_cursor
    def set_current_widget(self, widget):
        if self._ui.stackedWidget.indexOf(widget) <= 0:
            self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def current_widget(self):
        return self._ui.stackedWidget.currentWidget()

    def closeEvent(self, event):
        self.quit_application()

    def _maybe_restart_application(self, asker='plugins'):
        QtWidgets.QMessageBox.warning(self,
                                      'Change detected',
                                      f'A change in the {asker} has been detected, you may have to restart the appplication to see the effect.',
                                      QtWidgets.QMessageBox.Ok)

    def confirm_close(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.workflowManager().isModified():
            ret = QtWidgets.QMessageBox.warning(self,
                                                'Unsaved Changes',
                                                'You have unsaved changes, would you like to save these changes now?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                self._model.workflowManager().save()

    def quit_application(self):
        self.confirm_close()

        self._model.setSize(self.size())
        self._model.setPos(self.pos())
        self._model.writeSettings()
        QtGui.QGuiApplication.quit()

    def about(self):
        from mapclient.view.dialogs.about.aboutdialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def _show_log_information_dialog(self):
        from mapclient.view.dialogs.log.loginformation import LogInformation
        dlg = LogInformation(self)
        dlg.fillTable(self)
        dlg.setModal(True)
        dlg.exec_()

    def show_options_dialog(self, current_tab=0):
        from mapclient.view.managers.options.optionsdialog import OptionsDialog

        om = self._model.optionsManager()
        options = om.getOptions()
        dlg = OptionsDialog(self)
        dlg.setCurrentTab(current_tab)
        dlg.load(options)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            if dlg.isModified():
                om.setOptions(dlg.save())

        # set availability of functionality.
        pm = self._model.pluginManager()
        self._action_PluginWizard.setEnabled(dlg.checkedOk(WIZARD_TOOL_STRING))
        self._action_PMR.setEnabled(dlg.checkedOk(PMR_TOOL_STRING))
        self._workflowWidget.applyOptions()

    def _show_package_manager_dialog(self):
        from mapclient.view.managers.package.packagemanagerdialog import PackageManagerDialog
        pm = self._model.package_manager()

        dlg = PackageManagerDialog(self)
        dlg.set_directories(pm.directories())
        dlg.setModal(True)
        if dlg.exec_():
            pm.set_directories(dlg.directories())
            if pm.is_modified():
                pm.load()
                self._maybe_restart_application(asker='packages')

    def _show_plugin_manager_dialog(self):
        from mapclient.view.managers.plugins.pluginmanagerdialog import PluginManagerDialog
        pm = self._model.pluginManager()
        #         pluginErrors = pm.getPluginErrors()
        #         print(pluginErrors)
        dlg = PluginManagerDialog(self._model.pluginManager()._ignoredPlugins,
                                  self._model.pluginManager()._doNotShowPluginErrors,
                                  self._model.pluginManager()._resourceFiles,
                                  self._model.pluginManager()._updaterSettings,
                                  self._model.pluginManager()._unsuccessful_package_installations, self)
        self._pluginManagerDlg = dlg
        dlg.setDirectories(pm.directories())
        dlg.setLoadDefaultPlugins(pm.loadDefaultPlugins())
        dlg.reloadPlugins = self._plugin_manager_load_plugins

        dlg.setModal(True)
        if dlg.exec_():
            pm._ignoredPlugins = dlg._ignoredPlugins
            pm._doNotShowPluginErrors = dlg._do_not_show_plugin_errors
            pm._resourceFiles = dlg._resource_filenames
            pm._updaterSettings = dlg._updaterSettings
            if self._plugin_manager_load_plugins():
                self._maybe_restart_application()

        self._pluginManagerDlg = None

    @set_wait_cursor
    def _plugin_manager_load_plugins(self):
        """
        Get the plugin manager to load the current plugins.

        Returns True if the plugin manager reloaded plugins, False otherwise.
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

            return True

        return False

    def _create_qt_tools_options(self):
        om = self._model.optionsManager()
        return {USE_EXTERNAL_RCC: om.getOption(USE_EXTERNAL_RCC),
                PYSIDE_RCC_EXE: om.getOption(PYSIDE_RCC_EXE),
                PYSIDE_UIC_EXE: om.getOption(PYSIDE_UIC_EXE),
                USE_EXTERNAL_UIC: om.getOption(USE_EXTERNAL_UIC)}

    def _show_plugin_wizard_dialog(self):
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

            s = Skeleton(dlg.getOptions(), self._create_qt_tools_options())
            try:
                s.write()
                pm = self._model.pluginManager()
                pm.setReloadPlugins()
                self._plugin_manager_load_plugins()
                QtWidgets.QMessageBox.information(self, 'Skeleton Step', 'The Skeleton step has successfully been written to disk.')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error Writing Step', 'There was an error writing the step, perhaps the step already exists?')
                logger.critical(e)
                import os
                package_directory = s.getPackageDirectory()
                if os.path.exists(package_directory):
                    logger.info('Removing partially created skeleton step "{0}"'.format(package_directory))
                    import shutil
                    shutil.rmtree(package_directory)

    def _show_rename_plugin_dialog(self):
        from mapclient.tools.renameplugin.renamedialog import RenameDialog

        om = self._model.optionsManager()
        dlg = RenameDialog(om.getOption(PYSIDE_RCC_EXE), self)
        dlg.setModal(True)
        dlg.exec_()

    def _show_update_workflow_dialog(self):
        from mapclient.tools.updateworkflow.updateworkflowdialog import UpdateWorkflowDialog

        om = self._model.optionsManager()
        dlg = UpdateWorkflowDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def _show_pmr_tool(self):
        om = self._model.optionsManager()
        from mapclient.tools.pmr.dialogs.register import PMRRegisterDialog
        dlg = PMRRegisterDialog(om.getOption(USE_EXTERNAL_GIT), self)
        dlg.setModal(True)
        dlg.exec_()

    def _show_annotation_tool(self):
        from mapclient.tools.annotation.annotationdialog import AnnotationDialog
        location = self._model.workflowManager().location()
        dlg = AnnotationDialog(location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, self)
        dlg.setModal(True)
        dlg.exec_()

    def _show_map_icon_dialog(self):
        from mapclient.tools.mapicon.mapicondialog import MAPIconDialog
        location = self._model.workflowManager().location()
        dlg = MAPIconDialog(location, self)
        dlg.setModal(True)
        if dlg.exec_():
            dlg.createIcon()

    def _show_plugin_errors_dialog(self):
        pm = self._model.pluginManager()
        if pm.haveErrors():
            return
            # dlg = PluginErrors(pm.getPluginErrors(), pm.getIgnoredPlugins(), pm.getResourceFiles(), pm.getUpdaterSettings())
            # if not self._doNotShowPluginErrors:
            #     dlg.setModal(True)
            #     dlg.fillList()
            #     dlg.exec_()
            # ignored_plugins = dlg.getIgnoredPlugins()
            # for plugin in ignored_plugins:
            #     if plugin not in self._ignoredPlugins:
            #         self._ignoredPlugins += [plugin]
            # if dlg._doNotShow:
            #     self._doNotShowPluginErrors = True
            # if dlg._hotfixExecuted:
            #     self.load()
