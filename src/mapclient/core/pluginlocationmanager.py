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

class PluginLocationManager:
    '''
    Manages plugin information for the current workflow.
    '''

    _plugin_database = {}
            
    def saveState(self, ws, scene):
        ws.remove('required_plugins')            
        ws.beginGroup('required_plugins')
        ws.beginWriteArray('plugin')
        pluginIndex = 0
        for item in scene._items:
            if item.Type == 'Step':
                step_name = item._step.getName()
                if step_name in self._plugin_database.keys():
                    information_dict = self._plugin_database[step_name]
                    ws.setArrayIndex(pluginIndex)
                    ws.setValue('name', step_name)
                    ws.setValue('author', information_dict['author'])
                    ws.setValue('version', information_dict['version'])
                    ws.setValue('location', information_dict['location'])
                    ws.setValue('dependencies', information_dict['dependencies'])
                    pluginIndex += 1
        ws.endArray()
        ws.endGroup()
        
    def addLoadedPluginInformation(self, plugin_name, step_name, plugin_author, plugin_version, plugin_location, plugin_dependencies):
        plugin_dict = {}
        plugin_dict['plugin name'] = plugin_name
        plugin_dict['author'] = plugin_author
        plugin_dict['version'] = plugin_version
        plugin_dict['location'] = plugin_location
        plugin_dict['dependencies'] = plugin_dependencies
        self._plugin_database[step_name] = plugin_dict
        
    def getPluginDatabase(self):
        return self._plugin_database
