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
        
    def fillTable(self, plugin_information):
        for plugin in plugin_information.keys():
            display_string = plugin + ' - ' + 'Author: ' + plugin_information[plugin]['author'] + ' | ' + \
                                'Version: ' + plugin_information[plugin]['version'] + ' | ' + 'Location: ' + \
                                plugin_information[plugin]['location']
            self._ui.requiredPlugins.addItem(display_string)