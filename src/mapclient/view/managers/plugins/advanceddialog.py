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
import pkgutil
import os
import sys
import collections

from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QFileDialog
from PySide2.QtCore import Qt

from mapclient.view.managers.plugins.ui.ui_advanceddialog import Ui_AdvancedDialog
from mapclient.view.managers.plugins.pluginupdater import PluginUpdater
from mapclient.view.utils import set_wait_cursor
from mapclient.settings.definitions import PLUGINS_PACKAGE_NAME
import importlib


class AdvancedDialog(QDialog):
    """
    Dialog containing advanced plugin tools, settings and information.
    """

    def __init__(self, ignored_plugins, do_not_show_errors, resource_files, updater_settings, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_AdvancedDialog()
        self._ui.setupUi(self)
        self._makeConnections()
        self._recommendedPlugins = 0  # need to implement
        self._installedPlugins = 0  # need to implement
        self.fillInstalledPackagesList()
        self._setupToolTips()
        self._pluginUpdater = PluginUpdater()
        self._plugins_to_update = {}
        self._ui.updateAllButton.setEnabled(False)
        self._ui.updateButton.setEnabled(False)
        self._ui.label_2.setText('Please analyse your plugins to check for updates.')

        self._updaterSettings = updater_settings
        self.setUpdaterSettings()

        self._resourceFiles = resource_files
        self.fillResourcesList()
        self.resourceFilenameLineEdit()

        self._ignoredPlugins = ignored_plugins
        self.fillIgnoreList()

        self._doNotShowErrors = do_not_show_errors
        self.setErrorsCheckBox()

        self._2to3Directory = self._pluginUpdater.locate2to3Script()
        if self._2to3Directory:
            self._ui.dir2to3.setText(self._2to3Directory)

        # will need ot modify
        if self._ui.virtEnvLocation.text() == 'a':
            self._ui.modifyVELocation.setText('Setup')

    def _makeConnections(self):
        self._ui.updateButton.clicked.connect(self.updatePlugins)
        self._ui.analyseButton.clicked.connect(self.analysePlugins)
        self._ui.updateAllButton.clicked.connect(self.updateAllPlugins)
        self._ui.listWidget.itemSelectionChanged.connect(self._pluginSelectionChanged)
        self._ui.tabWidget.currentChanged.connect(self.fillUpdatesList)
        self._ui.locateButton.clicked.connect(self.locate2to3Script)
        self._ui.indentCheckBox.stateChanged.connect(self.indentSettings)
        self._ui.syntaxCheckBox.stateChanged.connect(self.syntaxSettings)
        self._ui.resourceCheckBox.stateChanged.connect(self.resourceSettings)
        self._ui.locationCheckBox.stateChanged.connect(self.locationSettings)
        self._ui.revertButton.clicked.connect(self.revertIgnoredPlugins)
        self._ui.showPluginErrors.stateChanged.connect(self.setShowPluginErrors)
        self._ui.dir2to3.textEdited.connect(self.set2to3Location)
        self._ui.ignoreList.itemSelectionChanged.connect(self._ignoredPluginSelectionChanged)
        self._ui.lineEdit.textEdited.connect(self.resourceFilenameLineEdit)
        self._ui.addResource.clicked.connect(self.addResourceFilename)
        self._ui.removeResource.clicked.connect(self.removeResourceFilename)
        self._ui.resourceList.itemSelectionChanged.connect(self._resourceFilenamesSelectionChanged)
        self._ui.listWidget.doubleClicked.connect(self.updatePlugins)
        self._ui.defaultVELocationCheckBox.stateChanged.connect(self.virtEnvLocation)
        self._ui.modifyVELocation.clicked.connect(self.modifyVELocation)
        self._ui.syntaxUpdatesCheckBox.stateChanged.connect(self.packageSyntaxUpdates)
        self._ui.virtualenvCheckBox.stateChanged.connect(self.installVirtualEnv)
        self._ui.installPackages.clicked.connect(self.installSelectedPackages)
        self._ui.uninstallPackages.clicked.connect(self.uninstallSelectedPackages)
        self._ui.packageInformation.clicked.connect(self.displayPackageInfo)
        self._ui.updatePackages.clicked.connect(self.updateSelectedPackages)
        self._ui.installedPackagesList.itemSelectionChanged.connect(self._installedPackagesSelectionChanged)
        self._ui.recommendedPackagesList.itemSelectionChanged.connect(self._recommendedPackagesSelectionChanged)
        self._ui.failedInstallsButton.clicked.connect(self.displayFailedPackageInstalls)

    def fillInstalledPackagesList(self):
        # virt_env_dir = self._ui.virtEnvLocation.text()
        # need to change so that have list stored within applicarion settings that is uodated every time a package is installed - much faster to load
        """
        virt_env_dir = 'C:\\Users\\Jonathan\\AppData\\Roaming\\Musculo Skeletal\\MAP Client\\pluginVirtEnv'
        output = subprocess.check_output([virt_env_dir + '\Scripts' + '\python.exe', virt_env_dir + '\Scripts' + '\pip.exe', 'list'], shell=True)
        installed_packages = output.decode('utf-8').split('\n')

        count = 0
        for package in installed_packages[:-1]:
            package_name = package.split()[0]
            toolTip = subprocess.check_output([virt_env_dir + '\Scripts\python.exe', virt_env_dir + '\Scripts\pip.exe', 'show', package_name], shell=True)
            toolTip = toolTip.decode('utf-8')
            self._ui.installedPackagesList.addItem(package[:-1])
            item = self._ui.installedPackagesList.item(count)
            item.setToolTip(toolTip)
        """

    def fillRecommendedPackagesList(self):
        # based on list of deependencies from existing plugins and analysing the index list of packages availble through pip
        # also stored in application settings for faster loading - updated with every version release (maybe include an automatic update button? - contact server?)
        pass

    def displayFailedPackageInstalls(self):
        # implement separate dialog with list of install fails. Analyse corresponding log and package info
        # --> give helpful tips in tooltips. Also give option to try install using wheels.
        pass

    def _recommendedPackagesSelectionChanged(self):
        if len(self._ui.recommendedPackagesList.selectedItems()) > 0 and len(self._ui.recommendedPackagesList.selectedItems()) != len(self._recommendedPlugins):
            self._ui.installPackages.setText('Install(' + str(len(self._ui.recommendedPackagesList.selectedItems())) + ')')
            self._ui.installPackages.setEnabled(True)
            if len(self._ui.recommendedPackagesList.selectedItems()) == 1:
                self._ui.packageInformation.setEnabled(True)
        elif (len(self._ui.ignoreList.selectedItems()) == len(self._recommendedPlugins) or len(self._ui.recommendedPackagesList.selectedItems()) == 0) and self._ui.recommendedPackagesList.count() > 0:
            self._ui.installPackages.setText('Install All')
            self._ui.installPackages.setEnabled(True)
            self._ui.packageInformation.setEnabled(False)
        else:
            self._ui.installPackages.setText('Install')
            self._ui.installPackages.setEnabled(False)
            self._ui.packageInformation.setEnabled(False)

    def _installedPackagesSelectionChanged(self):
        if len(self._ui.installedPackagesList.selectedItems()) > 0 and len(self._ui.installedPackagesList.selectedItems()) != len(self._installedPlugins):
            self._ui.uninstallPackages.setText('Uninstall(' + str(len(self._ui.installedPackagesList.selectedItems())) + ')')
            self._ui.uninstallPackages.setEnabled(True)
            self._ui.updatePackages.setText('Update(' + str(len(self._ui.installedPackagesList.selectedItems())) + ')')
            self._ui.updatePackages.setEnabled(True)
        elif (len(self._ui.ignoreList.selectedItems()) == len(self._recommendedPlugins) or len(self._ui.installedPackagesList.selectedItems()) == 0) and self._ui.installedPackagesList.count() > 0:
            self._ui.uninstallPackages.setText('Uninstall All')
            self._ui.uninstallPackages.setEnabled(True)
            self._ui.updatePackages.setText('Update All')
            self._ui.updatePackages.setEnabled(True)
        else:
            self._ui.uninstallPackages.setText('Uninstall')
            self._ui.uninstallPackages.setEnabled(False)
            self._ui.updatePackages.setText('Update')
            self._ui.updatePackages.setEnabled(False)

    def virtEnvLocation(self):
        # setting that sets the default location for the setup of the virtual environment for the appplication.
        # when unchecked the user must choose an alternative location to be used as the default
        pass

    def modifyVELocation(self):
        # enables user to completely move the virtual environment setup for the application (including all contents and installed packages)
        # also updates the sys.path so that the system is aware of packages in the VE (+updates any other required links - may need to change some API to deal with modified VE location)
        pass

    def packageSyntaxUpdates(self):
        # enables analysis of installed packages for syntax updates with the users run-time python version (3+)
        # once analysis has been performed the packages that could be updated (using same method as in the plugin updater)
        # will be highlighted in the list of installed packages (so user can clearly see which ones they can update)
        pass

    def installVirtualEnv(self):
        # setting that determines if the package 'virtualenv' is installed (if not already present in the user's system)
        # automatically while the application VE is bein setup
        pass

    def installSelectedPackages(self):
        # attemps to install the selected packages
        pass

    def uninstallSelectedPackages(self):
        # attempts to uninstall the selected packages
        pass

    def displayPackageInfo(self):
        # displays more detailed information about a particular recommended package including recommendatios
        # for use and reasons why is has been recommended
        pass

    def updateSelectedPackages(self):
        # attempts to update the selected packages (these should have some indication to the user that they are outdated)
        pass

    def _setupToolTips(self):
        self._ui.analyseButton.setToolTip('Analyse plugins in your plugin directories for a range of updates.')
        self._ui.removeResource.setToolTip('Delete the selected resource filename.')
        self._ui.addResource.setToolTip('Add a resource filename.')
        self._ui.revertButton.setToolTip('Revert previously ignored plugin errors.')
        self._ui.ignoreList.setToolTip('Plugins with errors that have previously been ignored.')
        self._ui.resourceList.setToolTip('List of resource filenames used in your plugins.')
        self._ui.syntaxCheckBox.setToolTip('Enable syntax updates.')
        self._ui.resourceCheckBox.setToolTip('Enable resource file updates.')
        self._ui.locationCheckBox.setToolTip('Enable location information updates.')
        self._ui.indentCheckBox.setToolTip('Enable indentation updates.')

    def setUpdaterSettings(self):
        self._ui.syntaxCheckBox.setChecked(self._updaterSettings['syntax'])
        self._ui.indentCheckBox.setChecked(self._updaterSettings['indentation'])
        self._ui.locationCheckBox.setChecked(self._updaterSettings['location'])
        self._ui.resourceCheckBox.setChecked(self._updaterSettings['resources'])

    def removeResourceFilename(self):
        revert_index = 0
        for item in self._ui.resourceList.selectedItems():
            for index in range(len(self._resourceFiles)):
                    if item.text() == self._resourceFiles[index]:
                            revert_index = index
                            break
            self._resourceFiles.pop(revert_index)
        self.fillResourcesList()

    def addResourceFilename(self):
        if self._ui.lineEdit.text():
            self._resourceFiles.append(self._ui.lineEdit.text())
            self._ui.resourceList.addItem(self._ui.lineEdit.text())
        self._ui.lineEdit.clear()

    def fillResourcesList(self):
        self._ui.resourceList.clear()
        if self._resourceFiles:
            for filename in self._resourceFiles:
                self._ui.resourceList.addItem(filename)

        self._resourceFilenamesSelectionChanged()

    def _resourceFilenamesSelectionChanged(self):
        if self._ui.resourceList.count() == 0 or len(self._ui.resourceList.selectedItems()) == 0:
            self._ui.removeResource.setEnabled(False)
        else:
            self._ui.removeResource.setEnabled(True)

    def resourceFilenameLineEdit(self):
        if self._ui.lineEdit.text():
            self._ui.addResource.setEnabled(True)
        else:
            self._ui.addResource.setEnabled(False)

    def fillIgnoreList(self):
        self._ui.ignoreList.clear()
        if self._ignoredPlugins:
            for plugin in self._ignoredPlugins:
                self._ui.ignoreList.addItem(plugin)

        self._ignoredPluginSelectionChanged()

    def setErrorsCheckBox(self):
        self._ui.showPluginErrors.setChecked(not self._doNotShowErrors)

    def _ignoredPluginSelectionChanged(self):
        if len(self._ui.ignoreList.selectedItems()) > 0 and len(self._ui.ignoreList.selectedItems()) != len(self._ignoredPlugins):
            self._ui.revertButton.setText('Revert(' + str(len(self._ui.ignoreList.selectedItems())) + ')')
            self._ui.revertButton.setEnabled(True)
        elif (len(self._ui.ignoreList.selectedItems()) == len(self._ignoredPlugins) or len(self._ui.ignoreList.selectedItems()) == 0) and self._ui.ignoreList.count() > 0:
            self._ui.revertButton.setText('Revert All')
            self._ui.revertButton.setEnabled(True)
        else:
            self._ui.revertButton.setText('Revert')
            self._ui.revertButton.setEnabled(False)

    def set2to3Location(self):
        self._2to3Directory = self._ui.dir2to3.text()

    def setShowPluginErrors(self):
        self._doNotShowErrors = not self._ui.showPluginErrors.isChecked()

    def revertIgnoredPlugins(self):
        revert_index = 0
        if len(self._ui.ignoreList.selectedItems()) == 0 and self._ui.ignoreList.count() != 0:
            for item_index in range(self._ui.ignoreList.count()):
                item = self._ui.ignoreList.item(item_index)
                for index in range(len(self._ignoredPlugins)):
                    if item.text() == self._ignoredPlugins[index]:
                        revert_index = index
                        break
                self._ignoredPlugins.pop(revert_index)
        else:
            for item in self._ui.ignoreList.selectedItems():
                for index in range(len(self._ignoredPlugins)):
                    if item.text() == self._ignoredPlugins[index]:
                            revert_index = index
                            break
                self._ignoredPlugins.pop(revert_index)
        self.fillIgnoreList()

    def indentSettings(self):
        self._updaterSettings['indentation'] = self._ui.indentCheckBox.isChecked()

    def syntaxSettings(self):
        self._updaterSettings['syntax'] = self._ui.syntaxCheckBox.isChecked()

    def locationSettings(self):
        self._updaterSettings['location'] = self._ui.locationCheckBox.isChecked()

    def resourceSettings(self):
        self._updaterSettings['resources'] = self._ui.resourceCheckBox.isChecked()

    def locate2to3Script(self):
        dir2to3Script = QFileDialog.getOpenFileName(self, dir=sys.exec_prefix, filter='Python scripts (*.py *.pyw)', caption='Locate Script', options=QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
        if len(dir2to3Script[0]) > 0:
            self._ui.dir2to3.setText(dir2to3Script[0])
            self.set2to3Location()

    def _pluginSelectionChanged(self):
        if len(self._ui.listWidget.selectedItems()) > 0 and len(self._ui.listWidget.selectedItems()) < self._ui.listWidget.count():
            self._ui.updateButton.setText('Update(' + str(len(self._ui.listWidget.selectedItems())) + ')')
            self._ui.updateButton.setEnabled(True)
        elif self._ui.listWidget.count() > 0:
            self._ui.updateAllButton.setEnabled(True)
            self._ui.updateButton.setText('Update')
            self._ui.updateButton.setEnabled(False)
        else:
            self._ui.updateAllButton.setEnabled(False)
            self._ui.updateButton.setText('Update')
            self._ui.updateButton.setEnabled(False)

    def _showDependencyUpdates(self):
        self._pluginUpdater._pluginUpdateDict = dict(list(self._pluginUpdater._pluginUpdateDict.items()) + list(self._pluginUpdater._dependenciesUpdateDict.items()))
        self.dependencySettings()
        self.fillUpdatesList()

    def check2to3Script(self):
        if not self._2to3Directory:
            self._ui.updateAllButton.setEnabled(False)
            self._ui.updateButton.setEnabled(False)
            self._ui.analyseButton.setEnabled(False)
            return True
        else:
            return False

    def fillUpdatesList(self):
        plugin_updates_dict = self._pluginUpdater._pluginUpdateDict
        self._ui.listWidget.clear()
        location_string = 'Location Update'
        resource_string = 'Resource Update'
        syntax_string = 'Syntax Update'
        indentation_string = 'Inconsistent Indentation'
        stringList = [location_string, resource_string, syntax_string, indentation_string]

        for plugin in plugin_updates_dict:
            display_string = plugin + ' - '
            for index in range(1, 5):
                update = plugin_updates_dict[plugin][index]
                if update:
                    display_string += stringList[index - 1] + ' | '
            if len(display_string) > (len(plugin) + 3):
                self._ui.listWidget.addItem(display_string[:-3])

        self._pluginSelectionChanged()

    def analysePlugins(self):
        if self.check2to3Script():
            self._ui.label_2.setText('2to3.py script not found.\nPlease locate it in the Options tab.')
            return
        else:
            self._pluginUpdater._pluginUpdateDict = {}
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            package = importlib.reload(sys.modules[PLUGINS_PACKAGE_NAME])
#             try:
#                 package = imp.reload(sys.modules['mapclientplugins'])
#             except Exception:
#                 package = importlib.reload(sys.modules['mapclientplugins'])
            for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
                if ispkg and modname != 'imagesourcestep' and modname != 'pointcloudserializerstep':
                    self._pluginUpdater._directory = _.path
                    (plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation, resourcesDirs, tabbed_modules) = performPluginAnalysis(_.path, modname, self._resourceFiles)
                    self._pluginUpdater.pluginUpdateDict(modname, plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                        plugin_tabbed_indentation, os.path.join(_.path, modname, '__init__.py'), resourcesDirs, tabbed_modules)
            self.fillUpdatesList()

            if self._ui.listWidget.count() == 0:
                self._ui.label_2.setText('None of your plugins require updates at this time.')
            else:
                self._ui.label_2.setText('Tip: Update a single plugin by double-clicking!')

    def updatePlugins(self):
        self._plugins_to_update = {}
        for plugin in self._ui.listWidget.selectedItems():
            plugin_name = plugin.text().split(' - ')[0]
            self._plugins_to_update[plugin_name] = self._pluginUpdater._pluginUpdateDict[plugin_name]
            del self._pluginUpdater._pluginUpdateDict[plugin_name]
        self.performUpdates()

    def updateAllPlugins(self):
        self._plugins_to_update = self._pluginUpdater._pluginUpdateDict
        self._pluginUpdater._pluginUpdateDict = {}
        self.performUpdates()

    def performUpdates(self):
        self._pluginUpdater.set2to3Dir(self._2to3Directory)
        plugins_not_updated, unsuccessful_updates = applyPluginUpdates(self._plugins_to_update, self._updaterSettings)

        if unsuccessful_updates:
            warning_string = '\n  The following plugins failed to update successfully:\n'
            for plugin in unsuccessful_updates:
                warning_string += '\n\t\t\t' + plugin
            QMessageBox.warning(self, 'Warning', warning_string + '\n\nPlease inspect the program logs for more information.  \t', QMessageBox.Ok)

        self._pluginUpdater._pluginUpdateDict = dict(list(plugins_not_updated.items()) + list(self._pluginUpdater._pluginUpdateDict.items()))
        self.fillUpdatesList()

def performPluginAnalysis(path, modname, resource_files):
    plugin_updater = PluginUpdater()
    plugin_resources_update, resourcesDirs = plugin_updater.checkResourcesUpdate(os.path.join(path, modname), resource_files)
    plugin_init_update = plugin_updater.checkPluginInitContents(os.path.join(path, modname, '__init__.py'))
    plugin_tabbed_indentation, tabbed_modules = plugin_updater.checkTabbedIndentation(path)
    if plugin_tabbed_indentation:
        plugin_updater.fixTabbedIndentation(modname, tabbed_modules, True)
    plugin_syntax_update = plugin_updater.checkModuleSyntax(path)
    plugin_updater.deleteTempFiles(tabbed_modules)

    return plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation, resourcesDirs, tabbed_modules

@set_wait_cursor
def applyPluginUpdates(plugins_to_update, updater_settings):
    plugin_updater = PluginUpdater()
    plugin_updater._pluginUpdateDict = plugins_to_update
    unsuccessful_updates = []
    plugins_to_delete = []
    for plugin in list(plugin_updater._pluginUpdateDict.keys()):
        if plugin_updater._pluginUpdateDict[plugin][4] and updater_settings['indentation']:
            plugin_updater.fixTabbedIndentation(plugin, plugin_updater._pluginUpdateDict[plugin][7], False)
        if (plugin_updater._pluginUpdateDict[plugin][3] and sys.version_info >= (3, 0)) and updater_settings['syntax']:
            plugin_updater.updateSyntax(plugin, plugin_updater._pluginUpdateDict[plugin][0])
        if plugin_updater._pluginUpdateDict[plugin][1] and updater_settings['location']:
            plugin_updater.updateInitContents(plugin, plugin_updater._pluginUpdateDict[plugin][5])
        if plugin_updater._pluginUpdateDict[plugin][2] and updater_settings['resources']:
            plugin_updater.updateResourcesFile(plugin, plugin_updater._pluginUpdateDict[plugin][6])

        compare = lambda required_updates, update_report: collections.Counter(required_updates) == collections.Counter(update_report)
        update_status = []
        update_status += [plugin_updater._pluginUpdateDict[plugin][1] and updater_settings['location']]
        update_status += [plugin_updater._pluginUpdateDict[plugin][2] and updater_settings['resources']]
        update_status += [plugin_updater._pluginUpdateDict[plugin][3] and updater_settings['syntax']]
        update_status += [plugin_updater._pluginUpdateDict[plugin][4] and updater_settings['indentation']]
        if compare(plugin_updater._pluginUpdateDict[plugin][1:5], [item for item in list(plugin_updater._successful_plugin_update.values())]):
            plugins_to_delete += [plugin]
        elif compare(update_status, [item for item in list(plugin_updater._successful_plugin_update.values())]):
            for index in range(len(update_status)):
                if update_status[index]:
                    plugin_updater._pluginUpdateDict[plugin][index + 1] = False
        else:
            unsuccessful_updates += [plugin]

        plugin_updater._successful_plugin_update = {'indentation_update_sucess':False, 'init_update_success':False, 'resources_update_success':False, 'syntax_update_success':False}

    for plugin in plugins_to_delete:
        del plugin_updater._pluginUpdateDict[plugin]

    return plugin_updater._pluginUpdateDict, unsuccessful_updates

