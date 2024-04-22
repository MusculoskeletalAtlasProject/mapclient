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
import sys
import traceback

from mapclient.core.utils import convert_exception_to_message, FileTypeObject
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.core.workflow.workflowitems import Connection, MetaStep
from mapclient.core.metrics import get_metrics_logger


logger = logging.getLogger(__name__)
metrics_logger = get_metrics_logger()


def _node_is_destination(graph, node):
    """
    Determine whether or not the given node features
    in a destination of another node.  Return True if
    the node is a destination, False otherwise..
    """
    for graph_node in graph:
        if node in graph[graph_node]:
            return True

    return False


def _find_starting_set(graph, nodes):
    """
    Find the set of all nodes that are connected but are
    not destinations for any other node.
    """
    starting_set = []
    for node in nodes:
        # Determine if node is a destination, if it is it is not a starting node
        if not _node_is_destination(graph, node):
            starting_set.append(node)

    return starting_set


def _determine_topological_order(graph, starting_set):
    """
    Determine the topological order of the graph.  Returns
    an empty list if the graph contains a loop.
    """
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
                if not _node_is_destination(temp_graph, m):
                    starting_set.append(m)

    # If the graph is not empty we have detected a loop,
    # or independent graphs.
    if temp_graph:
        return []

    return topologicalOrder


def _reverse_dict_with_lists(in_dict):
    reverseDictOut = {}
    for k, v in list(in_dict.items()):
        for rk in v:
            reverseDictOut[rk] = reverseDictOut.get(rk, [])
            reverseDictOut[rk].append(k)

    return reverseDictOut


class WorkflowDependencyGraph(object):

    def __init__(self, scene):
        self._scene = scene
        self._dependency_graph = {}
        self._reverse_dependency_graph = {}
        self._topological_order = []
        self._current = -1
        self._direction = 1
        self._finished_callback = None

    def _find_all_connected_nodes(self):
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

    def _calculate_dependency_graph(self):
        graph = {}
        for item in list(self._scene.items()):
            if item.Type == Connection.Type:
                graph[item.source()] = graph.get(item.source(), [])
                graph[item.source()].append(item.destination())

        return graph

    def _solo_node(self):
        scene_items = list(self._scene.items())
        if len(scene_items) == 1:
            scene_item = scene_items[0]
            if scene_item.Type == MetaStep.Type:
                return scene_item

        return None

    def _connections_for_nodes(self, source, destination):
        connections = []
        for item in list(self._scene.items()):
            if item.Type == Connection.Type:
                if item.source() == source and item.destination() == destination:
                    connections.append(item)

        return connections

    def set_finished_callback(self, callback):
        self._finished_callback = callback

    def can_execute(self):
        self._dependency_graph = self._calculate_dependency_graph()
        self._reverse_dependency_graph = _reverse_dict_with_lists(self._dependency_graph)
        # Find all connected nodes in the graph
        nodes = self._find_all_connected_nodes()
        # Find starting point set, uses helper graph
        starting_set = _find_starting_set(self._dependency_graph, nodes)

        self._topological_order = _determine_topological_order(self._dependency_graph, starting_set)

        items_count = len(self._scene.items())
        solo_node = self._solo_node()
        if solo_node:
            self._dependency_graph = {solo_node: []}
            self._topological_order = [solo_node]

        configured = [metastep.getStep().isConfigured() for metastep in self._topological_order]

        if not all(configured):
            return 1
        elif items_count == 0:
            return 2
        elif items_count > 1 and len(self._topological_order) == 0 and len(self._dependency_graph.keys()) == 0:
            return 3
        elif self._current != -1:
            return 4
        elif items_count > 1 and len(self._topological_order) == 0:
            return 5

        return 0

    def abort(self):
        self._current = -1

    def set_direction(self, direction):
        self._direction = 1 if direction else -1

    def execute(self):
        self._current += self._direction
        if self._current >= len(self._topological_order):
            self._current = -1
            if callable(self._finished_callback):
                self._finished_callback(True)
        elif self._current == -1:
            if callable(self._finished_callback):
                self._finished_callback(False)
        else:
            # Form input requirements
            current_node = self._topological_order[self._current]
            if current_node in self._reverse_dependency_graph:
                connections = []
                for node in self._reverse_dependency_graph[current_node]:
                    # Find connection information and extract outputs from steps
                    new_connections = self._connections_for_nodes(node, current_node)
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
                metrics_logger.plugin_executed(current_node.getStep().getName())
            except Exception as e:
                self._current = -1
                log_message = 'Exception caught while executing the workflow: ' + convert_exception_to_message(e)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                redirect_output = FileTypeObject()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=redirect_output)
                metrics_logger.error_occurred(current_node.getStep().getName(), str(exc_type))
                raise WorkflowError(log_message + '\n\n' + ''.join(redirect_output.messages))
