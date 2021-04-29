
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
from PySide2.QtCore import QObject

from mapclient.core.pluginframework import MetaQObjectPluginMountPoint

"""
Plugins can inherit this mount point in order to add to the menu of the GUI.

 A plugin that registers this mount point must have attributes
 * parent
 * menuLabel
 * menuName
 * actionLabel
 
 A plugin that registers this mount point could have attributes
 * subMenuLabel
 * subMenuName
 * shortcut
 * statustip
  
 It must implement
 * def execute(self):
 
 And it must call
 * QObject.__init__(self)
 in it's __init__ function
 """
MenuOptionMountPoint = MetaQObjectPluginMountPoint('MenuOptionMountPoint', (QObject,), {'subMenuLabel': None, 'subMenuName': None, 'shortcut': None, 'statustip': ''})

