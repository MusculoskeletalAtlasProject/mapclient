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
import os
import logging

from PySide import QtCore

from mapclient.core.workflow import WorkflowManager
from mapclient.core.undomanager import UndoManager
from mapclient.core.pluginframework import PluginManager

logger = logging.getLogger(__name__)

class MainApplication(object):
    '''
    This object is the main application object for the framework.
    '''


    def __init__(self):
        self._size = QtCore.QSize(600, 400)
        self._pos = QtCore.QPoint(100, 150)
        self._pluginManager = PluginManager()
        self._workflowManager = WorkflowManager()
        self._workflowManager.setPluginDatabase(self._pluginManager.getPluginDatabase())
        self._undoManager = UndoManager()
#         self._threadCommandManager = ThreadCommandManager()

    def setSize(self, size):
        self._size = size

    def size(self):
        return self._size

    def setPos(self, pos):
        self._pos = pos

    def pos(self):
        return self._pos

    def undoManager(self):
        return self._undoManager

    def workflowManager(self):
        return self._workflowManager

    def pluginManager(self):
        return self._pluginManager
    
    def writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self._size)
        settings.setValue('pos', self._pos)
        settings.endGroup()
        self._pluginManager.writeSettings(settings)
        self._workflowManager.writeSettings(settings)

    def readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self._size = settings.value('size', self._size)
        self._pos = settings.value('pos', self._pos)
        settings.endGroup()
        self._pluginManager.readSettings(settings)
        self._workflowManager.readSettings(settings)
