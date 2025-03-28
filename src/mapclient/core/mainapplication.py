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

from PySide6 import QtCore

from mapclient.core.managers.workflowmanager import WorkflowManager
from mapclient.core.managers.undomanager import UndoManager
from mapclient.core.managers.packagemanager import PackageManager
from mapclient.core.managers.pluginmanager import PluginManager
from mapclient.core.managers.optionsmanager import OptionsManager
from mapclient.core.checks import runChecks
from mapclient.settings.definitions import CHECK_TOOLS_ON_STARTUP, RECENTS_LENGTH
from mapclient.settings.general import get_settings

logger = logging.getLogger(__name__)


class MainApplication(object):
    """
    This object is the main application object for the framework.
    """

    def __init__(self):
        self._size = QtCore.QSize(600, 400)
        self._pos = QtCore.QPoint(100, 150)
        self._is_maximized = False
        self._recent_workflows = []
        self._pluginManager = PluginManager()
        self._package_manager = PackageManager()
        self._workflowManager = WorkflowManager(self)
        self._undoManager = UndoManager()
        self._optionsManager = OptionsManager()

    def installPackage(self, uri):
        self._pluginManager.installPackage(uri)

    def setSize(self, size):
        self._size = size

    def size(self):
        return self._size

    def setPos(self, pos):
        self._pos = pos

    def pos(self):
        return self._pos

    def set_maximized(self, is_maximized):
        self._is_maximized = is_maximized

    def is_maximized(self):
        return self._is_maximized

    def undoManager(self):
        return self._undoManager

    def workflowManager(self):
        return self._workflowManager

    def pluginManager(self):
        return self._pluginManager

    def package_manager(self):
        return self._package_manager

    def optionsManager(self):
        return self._optionsManager

    def doEnvironmentChecks(self):
        options = self._optionsManager.getOptions()
        return runChecks(options) if options[CHECK_TOOLS_ON_STARTUP] else True

    def writeSettings(self):
        settings = get_settings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self._size)
        settings.setValue('pos', self._pos)
        settings.setValue('is_maximized', self._is_maximized)
        settings.beginWriteArray('recent_workflows')
        for i, r in enumerate(self._recent_workflows):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        self._pluginManager.writeSettings(settings)
        self._workflowManager.writeSettings(settings)
        self._optionsManager.writeSettings(settings)
        self._package_manager.write_settings(settings)

    def readSettings(self):
        settings = get_settings()
        settings.beginGroup('MainWindow')
        self._size = settings.value('size', self._size)
        self._pos = settings.value('pos', self._pos)
        self._is_maximized = settings.value('is_maximized', 'true') == 'true'
        size = settings.beginReadArray('recent_workflows')
        for i in range(size):
            settings.setArrayIndex(i)
            self.add_recent_workflow(settings.value('item'))
        settings.endArray()
        settings.endGroup()

        self._pluginManager.readSettings(settings)
        self._workflowManager.readSettings(settings)
        self._optionsManager.readSettings(settings)
        self._package_manager.read_settings(settings)

    def add_recent_workflow(self, recent):
        recents_length = self._optionsManager.getOption(RECENTS_LENGTH)

        self.remove_recent_workflow(recent)
        while len(self._recent_workflows) >= recents_length:
            self._recent_workflows.pop(0)
        self._recent_workflows.append(recent)

    def remove_recent_workflow(self, recent):
        if recent in self._recent_workflows:
            index = self._recent_workflows.index(recent)
            del self._recent_workflows[index]

    def get_recent_workflows(self):
        return self._recent_workflows

    def clear_recent_workflows(self):
        self._recent_workflows = []

