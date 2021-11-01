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
from PySide2 import QtWidgets, QtCore

from mapclient.core.workflow.workflowscene import MetaStep, Connection
from mapclient.view.workflow.workflowgraphicsitems import Node, Arc
from mapclient.view.workflow.workflowcommands import CommandConfigure, CommandRemove


class WorkflowGraphicsScene(QtWidgets.QGraphicsScene):
    """
    This view side class is a non-authoratative representation
    of the current workflow scene model.  It must be kept in
    sync with the authoratative workflow scene model.
    """

    sceneWidth = 500
    sceneHeight = 1.618 * sceneWidth

    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, -self.sceneHeight // 2, -self.sceneWidth // 2, self.sceneHeight, self.sceneWidth, parent)
        self._workflow_scene = None
        self._previousSelection = []
        self._undoStack = None
        self._showStepNames = True
        self._is_ready = False

    def setReady(self):
        self._is_ready = True

    def setWorkflowScene(self, scene):
        self._workflow_scene = scene

    def workflowScene(self):
        return self._workflow_scene

    def setUndoStack(self, stack):
        self._undoStack = stack

    def addItem(self, item):
        QtWidgets.QGraphicsScene.addItem(self, item)
        if hasattr(item, 'Type'):
            if item.Type == Node.Type or item.Type == Arc.Type:
                self._workflow_scene.addItem(item.metaItem())

    def removeItem(self, item):
        QtWidgets.QGraphicsScene.removeItem(self, item)
        if hasattr(item, 'Type'):
            if item.Type == Node.Type:
                self._workflow_scene.removeItem(item.metaItem())
            elif item.Type == Arc.Type:
                item.sourceNode().removeArc(item)
                item.destinationNode().removeArc(item)
                self._workflow_scene.removeItem(item.metaItem())

    def updateModel(self):
        """
        Clears the QGraphicScene and re-populates it with what is currently
        in the WorkflowScene.
        """
        QtWidgets.QGraphicsScene.clear(self)
        meta_steps = {}
        connections = []
        for workflowitem in list(self._workflow_scene.items()):
            if workflowitem.Type == MetaStep.Type:
                node = Node(workflowitem)
                node.showStepName(self._showStepNames)
                workflowitem.getStep().registerConfiguredObserver(self.stepConfigured)
                workflowitem.getStep().registerDoneExecution(self.doneExecution)
                workflowitem.getStep().registerOnExecuteEntry(self.setCurrentWidget, self.setWidgetUndoRedoStack)
                workflowitem.getStep().registerIdentifierOccursCount(self.identifierOccursCount)
                # Put the node into the scene straight away so that the items scene will
                # be valid when we set the position.
                QtWidgets.QGraphicsScene.addItem(self, node)
                self.blockSignals(True)
                node.setPos(workflowitem.getPos())
                node.setSelected(workflowitem.getSelected())
                self.blockSignals(False)
                meta_steps[workflowitem] = node
            elif workflowitem.Type == Connection.Type:
                connections.append(workflowitem)

        for connection in connections:
            src_port_item = meta_steps[connection.source()]._step_port_items[connection.sourceIndex()]
            destination_port_item = meta_steps[connection.destination()]._step_port_items[connection.destinationIndex()]
            arc = Arc(src_port_item, destination_port_item)
            # Overwrite the connection created in the Arc with the original one that is in the
            # WorkflowScene
            arc._connection = connection
            # Again put the arc into the scene straight away so the scene will be valid
            QtWidgets.QGraphicsScene.addItem(self, arc)
            self.blockSignals(True)
            arc.setSelected(connection.getSelected())
            self.blockSignals(False)

        self._previousSelection = self.selectedItems()

    def ensureItemInScene(self, item, newPos):
        if self._is_ready:
            bRect = item.boundingRect()
            xp1 = bRect.x() + newPos.x()
            yp1 = bRect.y() + newPos.y()
            xp2 = bRect.x() + bRect.width() + newPos.x()
            yp2 = bRect.y() + bRect.height() + newPos.y()
            bRect.setCoords(xp1, yp1, xp2, yp2)
            rect = self.sceneRect()
            if not rect.contains(bRect):
                x1 = max(bRect.left(), rect.left()) + 2.0  # plus bounding rectangle adjust
                x2 = min(bRect.x() + bRect.width(), rect.x() + rect.width()) - bRect.width() + 2.0
                y1 = max(bRect.top(), rect.top()) + 2.0  # plus bounding rectangle adjust
                y2 = min(bRect.bottom(), rect.bottom()) - bRect.height() + 2.0
                if newPos.x() != x1:
                    newPos.setX(x1)
                elif newPos.x() != x2:
                    newPos.setX(x2)
                if newPos.y() != y1:
                    newPos.setY(y1)
                elif newPos.y() != y2:
                    newPos.setY(y2)

        return newPos

    def clear(self):
        QtWidgets.QGraphicsScene.clear(self)
        self._workflow_scene.clear()

    def previouslySelectedItems(self):
        return self._previousSelection

    def setPreviouslySelectedItems(self, selection):
        self._previousSelection = selection

    def commitChanges(self, location):
        self.parent().commitChanges(location)

    def setConfigureNode(self, node):
        self._currentConfigureNode = node
        self._currentConfigureNodeConfig = node.getConfig()

    def removeStep(self, node):
        self._undoStack.push(CommandRemove(self, [node]))

    def stepConfigured(self):
        new_config = self._currentConfigureNode.getConfig()
        if self._currentConfigureNodeConfig != new_config:
            self._undoStack.push(CommandConfigure(self, self._currentConfigureNode, new_config, self._currentConfigureNodeConfig))

    def setCurrentWidget(self, widget):
        # self.parent().set_current_widget(widget)
        self.parent().setCurrentWidget(widget)

    def setWidgetUndoRedoStack(self, stack):
        self.parent().setWidgetUndoRedoStack(stack)

    def showStepNames(self, show):
        self._showStepNames = show
        for workflow_item in list(self.items()):
            if hasattr(workflow_item, 'Type') and workflow_item.Type == Node.Type:
                workflow_item.showStepName(show)

    def doneExecution(self):
        self.parent().executeNext()

    def identifierOccursCount(self, identifier):
        return self.parent().identifierOccursCount(identifier)


