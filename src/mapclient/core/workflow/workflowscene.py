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
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.core.workflow.workflowitems import MetaStep, Connection
from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.utils import load_configuration
from mapclient.settings.general import get_configuration_file


def determine_connections(ws, i):
    connections = []
    arcCount = ws.beginReadArray('connections')
    for j in range(arcCount):
        ws.setArrayIndex(j)
        connectedTo = int(ws.value('connectedTo'))
        connectedToIndex = int(ws.value('connectedToIndex'))
        connectedFromIndex = int(ws.value('connectedFromIndex'))
        selected = ws.value('selected', 'false') == 'true'
        connections.append((i, connectedFromIndex, connectedTo, connectedToIndex, selected))
    ws.endArray()

    return connections


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


def get_step_name_from_identifier(ws, target_identifier):
    ws.beginGroup('nodes')
    step_name = ''
    node_count = ws.beginReadArray('nodelist')
    i = 0
    while i < node_count and not step_name:
        ws.setArrayIndex(i)
        name = ws.value('name')
        identifier = ws.value('identifier')
        if identifier == target_identifier:
            step_name = name

        i += 1

    ws.endArray()
    ws.endGroup()

    return step_name


def create_from(wf, name_identifiers, connections, location):
    """
    Create a workflow from the given names at the given location.
    Returns a list of

    :param wf: Workflow settings object.
    :param name_identifiers: List of tuples consisting of step names and associated identifiers.
    :param connections: List of connections to make in the workflow.
    :param location: Location of the workflow on the local disk.
    :return: List of steps.
    """
    steps = []
    try:
        wf.beginGroup('nodes')
        wf.beginWriteArray('nodelist')
        for i, name_identifier in enumerate(name_identifiers):
            wf.setArrayIndex(i)
            step = workflowStepFactory(name_identifier[0], location)
            step.setIdentifier(name_identifier[1])
            meta_step = MetaStep(step)
            wf.setValue('name', step.getName())
            wf.setValue('position', meta_step.getPos())
            wf.setValue('selected', meta_step.getSelected())
            wf.setValue('identifier', meta_step.getIdentifier())
            wf.setValue('unique_identifier', meta_step.getUniqueIdentifier())

            wf.beginWriteArray('connections')
            for connection_index, connection in enumerate(connections[i]):
                wf.setArrayIndex(connection_index)
                wf.setValue('connectedFromIndex', connection[1])
                wf.setValue('connectedTo', connection[2])
                wf.setValue('connectedToIndex', connection[3])
                wf.setValue('selected', connection[4])

            wf.endArray()

            steps.append(step)

        wf.endArray()
        wf.endGroup()

    except ValueError:
        names = [name_identifier[0] for name_identifier in name_identifiers]
        raise WorkflowError(f'Could not create workflow from names: {names}')

    return steps


class WorkflowScene(object):
    """
    This is the authoritative model for the workflow scene.
    """

    def __init__(self, manager):
        self._manager = manager
        self._location = ''
        self._items = {}
        self._dependencyGraph = WorkflowDependencyGraph(self)
        self._main_window = None
        self._default_view_rect = QtCore.QRectF(0, 0, 1024, 880)
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

    def changeIdentifier(self, meta_step):
        if meta_step.getIdentifier() and meta_step.getStepIdentifier():
            self._manager.changeIdentifier(meta_step.getIdentifier(), meta_step.getStepIdentifier())
        meta_step.syncIdentifier()

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
                self.changeIdentifier(metastep)

            identifier = metastep.getIdentifier() or metastep.getUniqueIdentifier()
            step = metastep.getStep()
            step.createGitIgnore()
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
            step_names = _read_step_names(ws)
            for name in step_names:
                workflowStepFactory(name, self._location)

        except ValueError:
            loadable = False

        return loadable

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

    def load_state(self, ws, scene_rect):
        self.clear()
        ws.beginGroup('view')
        loaded_view_parameters = {
            'scale': float(ws.value('scale', '1.0')),
            'rect': ws.value('rect', self._default_view_rect),
            'transform': ws.value('transform')
        }
        ws.endGroup()

        # Scale the WorkflowScene view-parameters:
        current_rect = scene_rect
        loaded_rect = loaded_view_parameters['rect']

        scale_factor = loaded_view_parameters['scale']
        if scale_factor != 1.0:
            current_rect.setWidth(current_rect.width() / scale_factor)
            current_rect.setHeight(current_rect.height() / scale_factor)
        self._view_parameters = loaded_view_parameters

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
            configuration = load_configuration(self._location, identifier)
            step.deserialize(configuration)
            connections.extend(determine_connections(ws, i))
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

    def has_steps(self):
        for item in self._items:
            if item.Type == MetaStep.Type:
                return True

        return False

    def step_list(self, by='identifier'):
        steps = []
        for item in self._items:
            if item.Type == MetaStep.Type:
                if by == 'identifier':
                    steps.append(item.getIdentifier())
                elif by == 'name':
                    steps.append(item.getName())

        return list(set(steps)) if by == 'name' else steps

    def matching_identifiers(self, name):
        identifiers = []
        for item in self._items:
            if item.Type == MetaStep.Type and item.getName() == name:
                identifiers.append(item.getIdentifier())

        return identifiers

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
