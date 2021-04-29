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
from PySide2.QtWidgets import QDialog, QMessageBox

from mapclient.view.managers.plugins.advanceddialog import performPluginAnalysis, applyPluginUpdates
from mapclient.view.managers.plugins.ui.ui_pluginerrors import Ui_PluginErrors


class PluginErrors(QDialog):

    def __init__(self, plugins, ignored_plugins, resource_files, updater_settings, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_PluginErrors()
        self._ui.setupUi(self)
        self._makeConnections()
        self._resourceFiles = resource_files
        self._updaterSettings = updater_settings
        self._hotfixExecuted = False
        self._ui.label.setText('The following plugins could not be loaded correctly.\nHover over each plugin for suggested solutions.\nTo perfom a hotfix simply double-click a plugin.')

        self._pluginErrors = plugins
        self._plugin_directories = self._pluginErrors['directories']
        del self._pluginErrors['directories']

        self._ignoredPlugins = ignored_plugins
        self._doNotShow = False

    def _makeConnections(self):
        self._ui.ignoreButton.clicked.connect(self.ignoreSelectedPlugins)
        self._ui.listWidget.itemSelectionChanged.connect(self._pluginSelectionChanged)
        self._ui.hideCheckBox.stateChanged.connect(self.doNotShowDialogAgain)
        self._ui.listWidget.doubleClicked.connect(self.performQuickFixes)

    def fillList(self):
        self._ui.listWidget.clear()
        for error in self._pluginErrors:
            for plugin in self._pluginErrors[error]:
                if plugin not in self._ignoredPlugins:
                    self._ui.listWidget.addItem(plugin + ' - ' + error)

        for row in range(self._ui.listWidget.count()):
            item = self._ui.listWidget.item(row)
            text = item.text().split(' - ')
            error = text[-1]
            if error == 'TypeError' or error == 'SyntaxError' or error == 'TabError':
                item.setToolTip('Please update this plugin using the built-in\nplugin updater under \'Advanced\' in the Plugin Manager\ndialog.')
            else:
                item.setToolTip('Please examine the plugin README.md file and\nobtain the listed dependencies.')

            self._pluginSelectionChanged()

    def _pluginSelectionChanged(self):
        if len(self._ui.listWidget.selectedItems()) > 0:
            if len(self._ui.listWidget.selectedItems()) == self._ui.listWidget.count():
                self._ui.ignoreButton.setText('Ignore All')
            else:
                self._ui.ignoreButton.setText('Ignore(' + str(len(self._ui.listWidget.selectedItems())) + ')')
            self._ui.ignoreButton.setEnabled(True)
        else:
            self._ui.ignoreButton.setText('Ignore')
            self._ui.ignoreButton.setEnabled(False)

    def ignoreSelectedPlugins(self):
        for item in self._ui.listWidget.selectedItems():
            plugin = item.text().split(' - ')[0]
            self._ignoredPlugins += [plugin]

        self.fillList()

    def doNotShowDialogAgain(self):
        if self._ui.hideCheckBox.isChecked():
            self._doNotShow = True
        else:
            self._doNotShow = False

    def getIgnoredPlugins(self):
        temp = self._ignoredPlugins
        ignored_plugins = []
        for plugin in temp:
            ignored_plugins += [str(plugin)]
        return ignored_plugins

    def performQuickFixes(self):
        plugin_dict = {}
        plugin = self._ui.listWidget.selectedItems()[0].text().split(' - ')[0]
        plugin_directory = self.locatePluginForHotfix(plugin)
        plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation, resourcesDirs, tabbed_modules = performPluginAnalysis(plugin_directory, plugin, self._resourceFiles)
        plugin_dict[plugin] = [plugin_directory, plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation, os.path.join(plugin_directory, plugin, '__init__.py'), resourcesDirs, tabbed_modules]
        _, failure = applyPluginUpdates(plugin_dict)
        if failure:
            QMessageBox.warning(self, 'Warning', '\nCould not update plugin. Please examine program logs for more info.  \t', QMessageBox.Ok)
        else:
            self._ui.listWidget.takeItem(self._ui.listWidget.row(self._ui.listWidget.selectedItems()[0]))
            self._hotfixExecuted = True

    def locatePluginForHotfix(self, plugin):
        return self._plugin_directories[plugin]
