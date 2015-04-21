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
from PySide.QtGui import QDialog, QTableWidgetItem

from mapclient.widgets.ui_plugindownloader import Ui_pluginDownloader

class PluginDownloader(QDialog):
    '''
    Dialog showing the plugins required to run the desired workflow from PMR.
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_pluginDownloader()
        self._ui.setupUi(self)
        self._makeConnections()
        self._downloadPlugins = True
        self._downloadDependencies = True
        
    def _makeConnections(self):
        self._ui.dependencyDownload.stateChanged.connect(self.downloadDependencies)
        self._ui.pluginDownload.stateChanged.connect(self.downloadPlugins)
        
    def fillPluginTable(self, plugin_information):
        if not plugin_information.keys():
            self._ui.pluginDownload.setEnabled(False)
            self._ui.requiredPlugins.setEnabled(False)
            self._downloadPlugins = False
        for plugin in plugin_information.keys():
            display_string = plugin + ' - Author: ' + plugin_information[plugin]['author'] + ' | Version: ' + \
            plugin_information[plugin]['version'] + ' | Location: ' + plugin_information[plugin]['location']
            self._ui.requiredPlugins.addItem(display_string)
            
    def fillDependenciesTable(self, dependency_information):
        if not dependency_information.keys():
            self._ui.dependencyDownload.setEnabled(False)
            self._ui.requiredDependencies.setEnabled(False)
            self._downloadDependencies = False
        for plugin in dependency_information.keys():
            display_string = plugin + ' - '
            for dependency in dependency_information[plugin]:
                display_string += dependency + ' | '
            self._ui.requiredDependencies.addItem(display_string[:-3])
            
    def downloadDependencies(self):
        self._downloadDependencies = self._ui.dependencyDownload.isChecked()
    
    def downloadPlugins(self):
        self._downloadPlugins = self._ui.pluginDownload.isChecked()