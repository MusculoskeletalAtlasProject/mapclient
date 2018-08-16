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
import sys
import math
import logging

from PySide import QtCore, QtGui

from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.workflow.workflowscene import MetaStep
from mapclient.view.workflow.workflowcommands import CommandSelection, CommandRemove, CommandAdd, CommandMove
from mapclient.view.workflow.workflowgraphicsitems import Node, Arc, ErrorItem, ArrowLine, StepPort

logger = logging.getLogger()


class WorkflowGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self._selectedNodes = []
        self._errorIconTimer = QtCore.QTimer()
        self._errorIconTimer.setInterval(2000)
        self._errorIconTimer.setSingleShot(True)
        self._errorIconTimer.timeout.connect(self._errorIconTimeout)
        self._errorIcon = None

        self._main_window = None

        self._undoStack = None
        self._location = ''
        self._showStepNames = True

        self._connectLine = None
        self._connectSourceNode = None

        self._selectionStartPos = None

        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        grid_pic = QtGui.QPixmap(':/workflow/images/grid.png')
        self._grid_brush = QtGui.QBrush(grid_pic)

#        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
#        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)

    def clear(self):
        self.scene().clear()

    def setUndoStack(self, stack):
        self._undoStack = stack

    def setLocation(self, location):
        self._location = location

    def setMainWindow(self, main_window):
        self._main_window = main_window

    def showStepNames(self, show):
        self._showStepNames = show

    def connectNodes(self, node1, node2):
        # Check if nodes are already connected
        if not node1.hasArcToDestination(node2):
            if node1.canConnect(node2):
                command = CommandAdd(self.scene(), Arc(node1, node2))
                self._undoStack.push(command)
            else:
                # add temporary line ???
                if self._errorIconTimer.isActive():
                    self._errorIconTimer.stop()
                    self._errorIconTimeout()

                self._errorIcon = ErrorItem(node1, node2)
                self.scene().addItem(self._errorIcon)
                self._errorIconTimer.start()

    def selectionChanged(self):
        currentSelection = self.scene().selectedItems()
        previousSelection = self.scene().previouslySelectedItems()
        command = CommandSelection(self.scene(), currentSelection, previousSelection)
        self._undoStack.push(command)
        self.scene().setPreviouslySelectedItems(currentSelection)

    def nodeSelected(self, node, state):
        if state == True and node not in self._selectedNodes:
            self._selectedNodes.append(node)
        elif state == False and node in self._selectedNodes:
            found = self._selectedNodes.index(node)
            del self._selectedNodes[found]

        if len(self._selectedNodes) == 2:
            self.connectNodes(self._selectedNodes[0], self._selectedNodes[1])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            command = CommandRemove(self.scene(), self.scene().selectedItems())
            self._undoStack.push(command)
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.type() == Node.Type:
            item.showContextMenu(event.globalPos())

    def mousePressEvent(self, event):
        item = self.scene().itemAt(self.mapToScene(event.pos()))
        if event.button() == QtCore.Qt.RightButton:
            event.ignore()
        elif item and item.type() == StepPort.Type:
            centre = item.boundingRect().center()
            self._connectSourceNode = item
            self._connectLine = ArrowLine(QtCore.QLineF(item.mapToScene(centre),
                                         self.mapToScene(event.pos())))
            self.scene().addItem(self._connectLine)
        else:
            QtGui.QGraphicsView.mousePressEvent(self, event)
            self._selectionStartPos = event.pos()

    def mouseMoveEvent(self, event):
        if self._connectLine:
            newLine = QtCore.QLineF(self._connectLine.line().p1(), self.mapToScene(event.pos()))
            self._connectLine.setLine(newLine)
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self._connectLine:
            item = self.scene().itemAt(self.mapToScene(event.pos()))
            if item and item.type() == StepPort.Type:
                self.connectNodes(self._connectSourceNode, item)
            self.scene().removeItem(self._connectLine)
            self._connectLine = None
            self._connectSourceNode = None
        else:
            QtGui.QGraphicsView.mouseReleaseEvent(self, event)
            if self._selectionStartPos:
                diff = event.pos() - self._selectionStartPos
                if diff.x() != 0 and diff.y() != 0:
                    self._undoStack.beginMacro('Move Step(s)')
                    for item in self.scene().selectedItems():
                        if item.type() == Node.Type:
                            self._undoStack.push(CommandMove(item, item.pos() - diff, item.pos()))
                    self._undoStack.endMacro()

    def _errorIconTimeout(self):
        self.scene().removeItem(self._errorIcon)
        del self._errorIcon

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.EnabledChange:
            self.invalidateScene(self.sceneRect())

    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        rightShadow = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
            painter.fillRect(rightShadow, QtCore.Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
            painter.fillRect(bottomShadow, QtCore.Qt.darkGray)

        painter.setBrush(self._grid_brush)  # QtCore.Qt.NoBrush
        painter.drawRect(sceneRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            pieceData = event.mimeData().data("image/x-workflow-step")
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            hotspot = QtCore.QPoint()

            nameLen = stream.readUInt32()
            # name = stream.readRawData(nameLen).decode('utf-8')
            if sys.version_info < (3, 0):
                name = stream.readRawData(nameLen).decode('utf-8')
            else:
                buf = QtCore.QByteArray()
                stream >> buf
                name = '{0}'.format(buf)

            stream >> hotspot

            scene = self.scene()
            position = self.mapToScene(event.pos() - hotspot)
            step = workflowStepFactory(name, self._location)
            step.setMainWindow(self._main_window)
            metastep = MetaStep(step)
            node = Node(metastep)
            node.showStepName(self._showStepNames)
            metastep._step.registerConfiguredObserver(scene.stepConfigured)
            metastep._step.registerDoneExecution(scene.doneExecution)
            metastep._step.registerOnExecuteEntry(scene.setCurrentWidget)
            metastep._step.registerIdentifierOccursCount(scene.identifierOccursCount)

            self._undoStack.beginMacro('Add node')
            self._undoStack.push(CommandAdd(scene, node))
            # Set the position after it has been added to the scene
            self._undoStack.push(CommandMove(node, position, scene.ensureItemInScene(node, position)))
            scene.clearSelection()
            node.setSelected(True)
            self._undoStack.endMacro()

            self.setFocus()
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

        self.update()

#    def dragLeaveEvent(self, event):
#        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event):
        QtGui.QGraphicsView.resizeEvent(self, event)
        scene = self.scene()
        event_size = event.size()
        view_rect = QtCore.QRectF(0, 0, event_size.width(), event_size.height())
        items_rect = scene.itemsBoundingRect()
        items_rect.adjust(0, 0, 10, 10)

        scene_rect = view_rect.united(items_rect)
        scene.setSceneRect(10, 10, scene_rect.width() - 20, scene_rect.height() - 20)

    def wheelEvent(self, event):
        self._scaleView(math.pow(2.0, -event.delta() / 240.0))

    def _scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        transformation_anchor = self.transformationAnchor()
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.scale(scaleFactor, scaleFactor)
        self.setTransformationAnchor(transformation_anchor)


