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
from PySide2 import QtWidgets
from mapclient.view.managers.plugins.ui.ui_pluginmanagerdialog import Ui_PluginManagerDialog


class PluginManagerDialog(QtWidgets.QDialog):
    """
    Dialog for managing the list of plugin directories.
    """

    def __init__(self, ignored_plugins_list, do_not_show_plugin_errors, resource_filenames, updater_settings, unsuccessful_package_installations, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_PluginManagerDialog()
        self._ui.setupUi(self)
        self._ui.removeButton.setEnabled(False)
        self._ignoredPlugins = ignored_plugins_list
        self._do_not_show_plugin_errors = do_not_show_plugin_errors
        self._resource_filenames = resource_filenames
        self._updaterSettings = updater_settings
        self._unsuccessful_package_installations = unsuccessful_package_installations
        self._loadDefaultPlugins = True

        self._makeConnections()

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addDirectoryClicked)
        self._ui.directoryListing.itemSelectionChanged.connect(self._directorySelectionChanged)
        self._ui.removeButton.clicked.connect(self._removeButtonClicked)
        self._ui.reloadButton.clicked.connect(self.reloadPlugins)
        self._ui.advancedButton.clicked.connect(self.showAdvancedDialog)

    def showAdvancedDialog(self):
        from mapclient.view.managers.plugins.advanceddialog import AdvancedDialog
        dlg = AdvancedDialog(self._ignoredPlugins, self._do_not_show_plugin_errors, self._resource_filenames, self._updaterSettings)
        dlg.setModal(True)
        if dlg.exec_():
            self._ignoredPlugins = dlg._ignoredPlugins
            self._do_not_show_plugin_errors = dlg._doNotShowErrors
            self._resource_filenames = dlg._resourceFiles
            self._updaterSettings = dlg._updaterSettings
            self.reloadPlugins()

    def _directorySelectionChanged(self):
        self._ui.removeButton.setEnabled(len(self._ui.directoryListing.selectedItems()) > 0)

    def _removeButtonClicked(self):
        for item in self._ui.directoryListing.selectedItems():
            self._ui.directoryListing.takeItem(self._ui.directoryListing.row(item))

    def _addDirectoryClicked(self):
        selected_items = self._ui.directoryListing.selectedItems()
        last = ''
        if selected_items:
            last_selected_item = selected_items[-1]
            last = last_selected_item
        else:
            last = self._ui.directoryListing.item(self._ui.directoryListing.count() - 1)

        if last:
            last = last.text()

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select External Plugin Directory', dir=last, options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ReadOnly)
        if len(directory) > 0:
            self._ui.directoryListing.addItem(directory)

    def reloadPlugins(self):
        """
        Set this to a callable that will reload the plugins from the current plugin directories.
        """
        pass

    def setDirectories(self, directories):
        self._ui.directoryListing.addItems([directory for directory in directories if os.path.exists(directory)])

    def setLoadDefaultPlugins(self, loadDefaultPlugins):
        self._ui.defaultPluginCheckBox.setChecked(loadDefaultPlugins)

    def directories(self):
        directories = []
        for index in range(self._ui.directoryListing.count()):
            directories.append(self._ui.directoryListing.item(index).text())

        return directories

    def loadDefaultPlugins(self):
        return self._ui.defaultPluginCheckBox.isChecked()


class PluginDirectories(object):

    def __init__(self):
        self._previousLocation = ''
        self._defaultDirectory = True

    def previousLocation(self):
        return self._previousLocation

    def setPreviousLocation(self, previousLocation):
        self._previousLocation = previousLocation



