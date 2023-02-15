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
import uuid

from PySide6 import QtCore

from mapclient.core.workflow.workflowdependencygraph import WorkflowDependencyGraph
from mapclient.core.workflow.workflowitems import MetaStep, Connection
from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.utils import loadConfiguration
from mapclient.settings.general import get_configuration_file, get_restricted_plugins, restrict_plugins


class WorkflowScene(object):
    """
    This is the authoratative model for the workflow scene.
    """

    def __init__(self, manager):
        self._manager = manager
        self._location = ''
        self._items = {}
        self._dependencyGraph = WorkflowDependencyGraph(self)
        self._main_window = None
        self._view_parameters = None

    def getViewParameters(self):
        return self._view_parameters

    def setViewParameters(self, parameters):
        self._view_parameters = parameters

    def saveAnnotation(self, f):
        pass

    def updateWorkflowLocation(self, location):
        self._location = location
        update_made = False
        for meta_item in self._items:
            if meta_item.Type == MetaStep.Type:
                step = meta_item.getStep()
                step_location = step.getLocation()
                if step_location != location:
                    update_made = True
                    step.setLocation(location)
                    step.deserialize(step.serialize())

        return update_made

    def saveState(self, ws):
        connectionMap = {}
        stepList = []
        for item in self._items:
            if item.Type == MetaStep.Type:
                stepList.append(item)
            elif item.Type == Connection.Type:
                if item.source() in connectionMap:
                    connectionMap[item.source()].append(item)
                else:
                    connectionMap[item.source()] = [item]

        ws.beginGroup('view')
        for key in self._view_parameters:
            ws.setValue(key, self._view_parameters[key])
        ws.endGroup()

        ws.remove('nodes')
        ws.beginGroup('nodes')
        ws.beginWriteArray('nodelist')
        nodeIndex = 0
        for metastep in stepList:
            if metastep.hasIdentifierChanged():
                if metastep.getIdentifier() and metastep.getStepIdentifier():
                    self._manager.changeIdentifier(metastep.getIdentifier(), metastep.getStepIdentifier())
                metastep.syncIdentifier()

            identifier = metastep.getIdentifier() or metastep.getUniqueIdentifier()
            step = metastep.getStep()
            step_config = step.serialize()
            if step_config:
                with open(get_configuration_file(self._location, identifier), 'w') as f:
                    f.write(step_config)
            ws.setArrayIndex(nodeIndex)
            source_uri = step.getSourceURI()
            if source_uri is not None:
                ws.setValue('source_uri', source_uri)
            ws.setValue('name', step.getName())
            ws.setValue('position', metastep.getPos())
            ws.setValue('selected', metastep.getSelected())
            ws.setValue('identifier', identifier)
            ws.setValue('unique_identifier', metastep.getUniqueIdentifier())
            ws.beginWriteArray('connections')
            connectionIndex = 0
            if metastep in connectionMap:
                for connectionItem in connectionMap[metastep]:
                    ws.setArrayIndex(connectionIndex)
                    ws.setValue('connectedFromIndex', connectionItem.sourceIndex())
                    ws.setValue('connectedTo', stepList.index(connectionItem.destination()))
                    ws.setValue('connectedToIndex', connectionItem.destinationIndex())
                    ws.setValue('selected', connectionItem.getSelected())
                    connectionIndex += 1
            ws.endArray()
            nodeIndex += 1
        ws.endArray()
        ws.endGroup()

    def is_loadable(self, ws):
        loadable = True
        try:
            step_names = self._read_step_names(ws)
            for name in step_names:
                step = workflowStepFactory(name, self._location)

        except ValueError:
            loadable = False

        return loadable

    @staticmethod
    def _read_step_names(ws):
        ws.beginGroup('nodes')
        node_count = ws.beginReadArray('nodelist')

        step_names = set()
        for i in range(node_count):
            ws.setArrayIndex(i)
            name = ws.value('name')
            step_names.add(name)

        ws.endArray()
        ws.endGroup()

        return step_names

    def is_restricted(self, ws):
        step_names = self._read_step_names(ws)
        restricted_plugins = get_restricted_plugins()
        if len(step_names & restricted_plugins) != 0:
            return True

        return False

    def restrict_plugins(self, ws):
        step_names = self._read_step_names(ws)
        restrict_plugins(step_names)

    def fit_workflow(self, graphics_view, graphics_scene):
        """
        Scales the workflow items to fit into the current window size. This method maintains the aspect ratio of the saved workflow.
        """
        view_size = graphics_view.size()
        scene_size = graphics_scene.sceneRect()

        # -70 from both to account for step item width. +22 to scene to account for scene border.
        sf_x = (view_size.width() - 70) / (scene_size.width() - 48)
        sf_y = (view_size.height() - 70) / (scene_size.height() - 48)

        if sf_x != 1 or sf_y != 1:
            for item in self.items():
                if isinstance(item, MetaStep):
                    x = sf_x * item.getPos().x()
                    y = sf_y * item.getPos().y()
                    item.setPos(QtCore.QPointF(x, y))

            graphics_scene.setSceneRect(graphics_view.rect())
            graphics_scene.updateModel()

    def doStepReport(self, ws):
        report = {}
        ws.beginGroup('nodes')
        node_count = ws.beginReadArray('nodelist')
        for i in range(node_count):
            ws.setArrayIndex(i)
            name = ws.value('name')

            try:
                step = workflowStepFactory(name, self._location)
                report[name] = 'Found'

            except ValueError as e:
                plugin_manager = self._main_window.model().pluginManager()
                broken_plugins = plugin_manager.get_plugin_error_names()
                plugin_found = False
                for plugin in broken_plugins:
                    if plugin == name:
                        report[name] = 'Broken'
                        plugin_found = True
                if plugin_found:
                    continue

                source_uri = ws.value('source_uri', None)
                if source_uri is not None:
                    report[name] = source_uri
                else:
                    report[name] = 'Not Found - {0}'.format(e)

        ws.endArray()
        ws.endGroup()

        return report

    def load_state(self, ws):
        self.clear()
        ws.beginGroup('view')
        loaded_view_parameters = {
            'scale': float(ws.value('scale', '1.0')),
            'rect': ws.value('rect', self._view_parameters['rect']),
            'transform': ws.value('transform')
        }
        ws.endGroup()

        # Scale the WorkflowScene view-parameters:
        current_rect = self._view_parameters['rect']
        loaded_rect = loaded_view_parameters['rect']
        scale_factor = loaded_view_parameters['scale']
        if scale_factor != 1.0:
            current_rect.setWidth(current_rect.width() / scale_factor)
            current_rect.setHeight(current_rect.height() / scale_factor)
            self._view_parameters = {
                'scale': scale_factor,
                'rect': current_rect,
                'transform': loaded_view_parameters['transform']
            }
        sf_x = current_rect.width() / loaded_rect.width()
        sf_y = current_rect.height() / loaded_rect.height()

        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        metaStepList = []
        connections = []
        for i in range(nodeCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            position = ws.value('position')
            selected = ws.value('selected', 'false') == 'true'
            identifier = ws.value('identifier')
            uniqueIdentifier = ws.value('unique_identifier', uuid.uuid1())

            # Adjust the item positions according to the scale factors.
            position.setX(position.x() * sf_x)
            position.setY(position.y() * sf_y)

            step = workflowStepFactory(name, self._location)
            step.setMainWindow(self._main_window)
            step.registerIdentifierOccursCount(self.identifierOccursCount)
            metastep = MetaStep(step)
            metastep.setIdentifier(identifier)
            metastep.setUniqueIdentifier(uniqueIdentifier)
            metastep.setPos(position)
            metastep.setSelected(selected)
            metaStepList.append(metastep)
            self.addItem(metastep)

            # Deserialize after adding the step to the scene, this is so
            # we can validate the step identifier
            configuration = loadConfiguration(self._location, identifier)
            step.deserialize(configuration)
            arcCount = ws.beginReadArray('connections')
            for j in range(arcCount):
                ws.setArrayIndex(j)
                connectedTo = int(ws.value('connectedTo'))
                connectedToIndex = int(ws.value('connectedToIndex'))
                connectedFromIndex = int(ws.value('connectedFromIndex'))
                selected = ws.value('selected', 'false') == 'true'
                connections.append((i, connectedFromIndex, connectedTo, connectedToIndex, selected))
            ws.endArray()
        ws.endArray()
        ws.endGroup()
        for arc in connections:
            node1 = metaStepList[arc[0]]
            node2 = metaStepList[arc[2]]
            c = Connection(node1, arc[1], node2, arc[3])
            c._selected = arc[4]
            self.addItem(c)

    def setMainWindow(self, main_window):
        self._main_window = main_window

    def canExecute(self):
        return self._dependencyGraph.can_execute()

    def execute(self):
        self._dependencyGraph.execute()

    def abort_execution(self):
        self._dependencyGraph.abort()

    def set_workflow_direction(self, direction):
        self._dependencyGraph.set_direction(direction)

    def register_finished_workflow_callback(self, callback):
        self._dependencyGraph.set_finished_callback(callback)

    def registerDoneExecutionForAll(self, callback):
        for item in self._items:
            if item.Type == MetaStep.Type:
                item.getStep().registerDoneExecution(callback)

    def clear(self):
        self._items.clear()

    def items(self):
        return list(self._items.keys())

    def addItem(self, item):
        self._items[item] = item

    def removeItem(self, item):
        if item in self._items:
            del self._items[item]

    def setItemPos(self, item, pos):
        if item in self._items:
            self._items[item].setPos(pos)

    def setItemSelected(self, item, selected):
        if item in self._items:
            self._items[item].setSelected(selected)

    def identifierOccursCount(self, identifier):
        """
        Return the number of times the given identifier occurs in
        all the steps present in the workflow.  The count stops at two
        and returns indicating an excess number of the given identifier.
        An empty identifier will return the value 2 also, this is used
        to signify that the identifier is invalid.
        """
        if len(identifier) == 0:
            return 2

        identifier_occurrence_count = 0
        for key in self._items:
            item = self._items[key]
            if item.Type == MetaStep.Type and identifier == item.getIdentifier():
                identifier_occurrence_count += 1
                if identifier_occurrence_count > 1:
                    return identifier_occurrence_count

        return identifier_occurrence_count
