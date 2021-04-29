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
from PySide2.QtWidgets import QDialog

from mapclient.view.managers.plugins.ui.ui_plugindownloader import Ui_pluginDownloader


class PluginDownloader(QDialog):
    """
    Dialog showing the plugins required to run the desired workflow from PMR.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_pluginDownloader()
        self._ui.setupUi(self)
        self._downloadPlugins = True
        self._downloadDependencies = True

    def fillPluginTable(self, plugin_information):
        if not plugin_information:
            self._ui.pluginDownload.setEnabled(False)
            self._ui.requiredPlugins.setEnabled(False)
            self._downloadPlugins = False
        for plugin in plugin_information:
            self._ui.requiredPlugins.addItem(plugin)
            item = self._ui.requiredPlugins.item(self._ui.requiredPlugins.count() - 1)
            plugin_author = plugin_information[plugin]['author'] if plugin_information[plugin]['author'] else '<not set>'
            plugin_version = plugin_information[plugin]['version'] if plugin_information[plugin]['version'] else '<not set>'
            plugin_location = plugin_information[plugin]['location'] if plugin_information[plugin]['location'] else '<not set>'
            item.setToolTip('Author: ' + plugin_author + ', Version: ' + \
                            plugin_version + ', Location: ' + plugin_location)

    def fillDependenciesTable(self, dependency_information):
        if not dependency_information:
            self._ui.dependencyDownload.setEnabled(False)
            self._ui.requiredDependencies.setEnabled(False)
            self._downloadDependencies = False
        for dependency in dependency_information:
            self._ui.requiredDependencies.addItem(dependency)

    def downloadDependencies(self):
        return self._ui.dependencyDownload.isChecked()

    def installMissingPlugins(self):
        return self._ui.pluginDownload.isChecked()
