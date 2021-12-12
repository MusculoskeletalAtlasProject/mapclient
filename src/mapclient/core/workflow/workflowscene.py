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
import sys
import uuid
import logging
import traceback

from PySide2 import QtCore

from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.core.utils import convertExceptionToMessage, loadConfiguration, FileTypeObject
from mapclient.settings.general import get_configuration_file

logger = logging.getLogger(__name__)


class Item(object):

    def __init__(self):
        self._selected = True

    def getSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected


class MetaStep(Item):
    Type = 'Step'

    def __init__(self, step):
        Item.__init__(self)
        self._step = step
        self._pos = QtCore.QPointF(0, 0)
        self._uid = str(uuid.uuid1())
        self._id = step.getIdentifier()

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

    def getStep(self):
        return self._step

    def getName(self):
        return self._step.getName()

    def getIdentifier(self):
        if self._id:
            return self._id
        return self._uid

    def setIdentifier(self, identifier):
        self._step.setIdentifier(identifier)
        self._id = identifier

    def getStepIdentifier(self):
        identifier = self._step.getIdentifier()
        if identifier:
            return identifier
        return self._uid

    def hasIdentifierChanged(self):
        return not (self.getIdentifier() == self.getStepIdentifier())

    def syncIdentifier(self):
        self._id = self._step.getIdentifier()

    def getUniqueIdentifier(self):
        return self._uid

    def setUniqueIdentifier(self, uniqueIdentifier):
        # Awesome QSettings appears to be changing my string into a
        # uuid.UUID class
        if type(uniqueIdentifier) == uuid.UUID:
            self._uid = str(uniqueIdentifier)
        else:
            self._uid = uniqueIdentifier


class Connection(Item):
    Type = 'Connection'

    def __init__(self, source, sourceIndex, destination, destinationIndex):
        Item.__init__(self)
        self._source = source
        self._sourceIndex = sourceIndex
        self._destination = destination
        self._destinationIndex = destinationIndex

    def source(self):
        return self._source

    def sourceIndex(self):
        return self._sourceIndex

    def destination(self):
        return self._destination

    def destinationIndex(self):
        return self._destinationIndex


class WorkflowDependencyGraph(object):

    def __init__(self, scene):
        self._scene = scene
        self._dependencyGraph = {}
        self._reverseDependencyGraph = {}
        self._topologicalOrder = []
        self._current = -1

    def _findAllConnectedNodes(self):
        """
        Return a list of all the nodes that have a connection.
        """
        nodes = []
        for item in list(self._scene.items()):
            if item.Type == Connection.Type:
                if item.source() not in nodes:
                    nodes.append(item.source())
                if item.destination() not in nodes:
                    nodes.append(item.destination())

        return nodes

    def _nodeIsDestination(self, graph, node):
        """
        Determine whether or not the given node features
        in a destination of another node.  Return True if
        the node is a destination, False otherwise..
        """
        for graph_node in graph:
            if node in graph[graph_node]:
                return True

        return False

    def _findStartingSet(self, graph, nodes):
        """
        Find the set of all nodes that are connected but are
        not destinations for any other node.
        """
        starting_set = []
        for node in nodes:
            # Determine if node is a destination, if it is it is not a starting node
            if not self._nodeIsDestination(graph, node):
                starting_set.append(node)

        return starting_set

    def _determineTopologicalOrder(self, graph, starting_set):
        """
        Determine the topological order of the graph.  Returns
        an empty list if the graph contains a loop.
        """
        # Find topological order
        temp_graph = graph.copy()
        topologicalOrder = []
        while len(starting_set) > 0:
            node = starting_set.pop()
            topologicalOrder.append(node)
            if node in temp_graph:
                for m in temp_graph[node][:]:
                    temp_graph[node].remove(m)
                    if len(temp_graph[node]) == 0:
                        del temp_graph[node]
                    if not self._nodeIsDestination(temp_graph, m):
                        starting_set.append(m)

        # If the graph is not empty we have detected a loop,
        # or independent graphs.
        if temp_graph:
            return []

        return topologicalOrder

    def _calculateDependencyGraph(self):
        graph = {}
        for item in list(self._scene.items()):
            if item.Type == Connection.Type:
                graph[item.source()] = graph.get(item.source(), [])
                graph[item.source()].append(item.destination())

        return graph

    def _connectionsForNodes(self, source, destination):
        connections = []
        for item in list(self._scene.items()):
            if item.Type == Connection.Type:
                if item.source() == source and item.destination() == destination:
                    connections.append(item)

        return connections

    def canExecute(self):
        self._dependencyGraph = self._calculateDependencyGraph()
        self._reverseDependencyGraph = reverseDictWithLists(self._dependencyGraph)
        # Find all connected nodes in the graph
        nodes = self._findAllConnectedNodes()
        # Find starting point set, uses helper graph
        starting_set = self._findStartingSet(self._dependencyGraph, nodes)

        self._topologicalOrder = self._determineTopologicalOrder(self._dependencyGraph, starting_set)

        configured = [metastep for metastep in self._topologicalOrder if metastep.getStep().isConfigured()]
        can = len(configured) == len(self._topologicalOrder) and len(self._topologicalOrder) >= 0
        return can and self._current == -1

    def execute(self):
        self._current += 1
        if self._current >= len(self._topologicalOrder):
            self._current = -1
        else:
            # Form input requirements
            current_node = self._topologicalOrder[self._current]
            if current_node in self._reverseDependencyGraph:
                connections = []
                for node in self._reverseDependencyGraph[current_node]:
                    # Find connection information and extract outputs from steps
                    new_connections = self._connectionsForNodes(node, current_node)
                    connections.extend([c for c in new_connections if c not in connections])
                    if len(new_connections) == 0:
                        logger.critical('Connection in workflow not found, something has gone horribly wrong')
                        raise WorkflowError('Connection in workflow not found, something has gone horribly wrong')

                for connection in connections:
                    # Alternative indexing based on index of port based on type.
                    # But don't use this as it is not what is documented.
                    # source_step = connection.source()._step
                    # destination_step = current_node._step
                    # source_ports = [port for port in source_step._ports if port.hasProvides()]
                    # destination_ports = [port for port in destination_step._ports if port.hasUses()]
                    # source_data_index = source_ports.index(source_step._ports[connection.sourceIndex()])
                    # destination_data_index = destination_ports.index(destination_step._ports[connection.destinationIndex()])

                    # dataIn = source_step.getPortData(source_data_index)
                    # destination_step.setPortData(destination_data_index, dataIn)

                    dataIn = connection.source().getStep().getPortData(connection.sourceIndex())
                    current_node.getStep().setPortData(connection.destinationIndex(), dataIn)

            try:
                current_node.getStep().execute()
            except Exception as e:
                self._current = -1
                log_message = 'Exception caught while executing the workflow: ' + convertExceptionToMessage(e)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                redirect_output = FileTypeObject()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=redirect_output)
                raise WorkflowError(log_message + '\n\n' + ''.join(redirect_output.messages))


class WorkflowScene(object):
    """
    This is the authoratative model for the workflow scene.
    """

    def __init__(self, manager):
        self._manager = manager
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

        location = self._manager.location()
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
                with open(get_configuration_file(location, identifier), 'w') as f:
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

    def isLoadable(self, ws):
        loadable = True
        location = self._manager.location()
        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        try:
            for i in range(nodeCount):
                ws.setArrayIndex(i)
                name = ws.value('name')
                step = workflowStepFactory(name, location)

        except ValueError:
            loadable = False

        ws.endArray()
        ws.endGroup()
        return loadable

    def doStepReport(self, ws):
        report = {}
        location = self._manager.location()
        ws.beginGroup('nodes')
        node_count = ws.beginReadArray('nodelist')
        for i in range(node_count):
            ws.setArrayIndex(i)
            name = ws.value('name')

            try:
                step = workflowStepFactory(name, location)
                report[name] = 'Found'

            except ValueError as e:
                plugin_manager = self._main_window.model().pluginManager()
                broken_plugins = plugin_manager.get_plugin_error_names()
                plugin_found = False
                for plugin in broken_plugins:
                    if plugin == name:
                        report[name] = 'Broken'
                        plugin_found = True
                if plugin_found == True:
                    continue

                source_uri = ws.value('source_uri', None)
                if source_uri is not None:
                    report[name] = source_uri
                else:
                    report[name] = 'Not Found - {0}'.format(e)

        ws.endArray()
        ws.endGroup()

        return report

    def loadState(self, ws):
        self.clear()
        location = self._manager.location()
        ws.beginGroup('view')
        self._view_parameters = {
            'scale': float(ws.value('scale', '1.0')),
            'rect': ws.value('rect'),
            'transform': ws.value('transform')
        }
        ws.endGroup()

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

            step = workflowStepFactory(name, location)
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
            configuration = loadConfiguration(location, identifier)
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

    def manager(self):
        return self._manager

    def canExecute(self):
        return self._dependencyGraph.canExecute()

    def execute(self):
        self._dependencyGraph.execute()

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


def reverseDictWithLists(inDict):
    reverseDictOut = {}  # defaultdict(list)
    for k, v in list(inDict.items()):
        for rk in v:
            reverseDictOut[rk] = reverseDictOut.get(rk, [])
            reverseDictOut[rk].append(k)

    return reverseDictOut
