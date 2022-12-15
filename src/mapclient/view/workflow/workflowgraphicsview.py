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
import math
import logging

from PySide6 import QtCore, QtWidgets, QtGui

from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.workflow.workflowscene import MetaStep
from mapclient.view.workflow.workflowcommands import CommandSelection, CommandRemove, CommandAdd, CommandMove
from mapclient.view.workflow.workflowgraphicsitems import Node, Arc, ErrorItem, ArrowLine, StepPort

logger = logging.getLogger()


class WorkflowGraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, parent=None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self._selectedNodes = []
        self._errorIconTimer = QtCore.QTimer()
        self._errorIconTimer.setInterval(2000)
        self._errorIconTimer.setSingleShot(True)
        self._errorIconTimer.timeout.connect(self._errorIconTimeout)
        self._errorIcon = None

        self._main_window = None
        self._graphics_shown = False
        self._graphics_initialised = False
        self._graphics_scale_factor = 1.0

        self._undoStack = None
        self._location = ''
        self._showStepNames = True

        self._connectLine = None
        self._connectSourceNode = None

        self._selectionStartPos = None

        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        grid_pic = QtGui.QPixmap(':/workflow/images/grid.png')
        self._grid_brush = QtGui.QBrush(grid_pic)

        #        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        #        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)

    def getViewParameters(self):
        return {
            'scale': self._graphics_scale_factor,
            'rect': self.sceneRect(),
            'transform': self.transform()
        }

    def setViewParameters(self, parameters):
        self._graphics_scale_factor = parameters['scale']
        if parameters['rect'] is not None:
            scene = self.scene()
            scene.setSceneRect(parameters['rect'])
        if parameters['transform'] is not None:
            self.setTransform(parameters['transform'])

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

    def connectNodes(self, src_port, dest_port):
        # Check if nodes are already connected
        if not src_port.hasArcToDestination(dest_port):
            if src_port.canConnect(dest_port):
                command = CommandAdd(self.scene(), Arc(src_port, dest_port))
                self._undoStack.push(command)
            else:
                # add temporary line ???
                if self._errorIconTimer.isActive():
                    self._errorIconTimer.stop()
                    self._errorIconTimeout()

                self._errorIcon = ErrorItem(src_port, dest_port)
                self.scene().addItem(self._errorIcon)
                self._errorIconTimer.start()

    def selectionChanged(self):
        currentSelection = self.scene().selectedItems()
        previousSelection = self.scene().previouslySelectedItems()
        command = CommandSelection(self.scene(), currentSelection, previousSelection)
        self._undoStack.push(command)
        self.scene().setPreviouslySelectedItems(currentSelection)

    def nodeSelected(self, node, state):
        if state and node not in self._selectedNodes:
            self._selectedNodes.append(node)
        elif not state and node in self._selectedNodes:
            found = self._selectedNodes.index(node)
            del self._selectedNodes[found]

        if len(self._selectedNodes) == 2:
            self.connectNodes(self._selectedNodes[0], self._selectedNodes[1])

    def keyPressEvent(self, event):
        QtWidgets.QGraphicsView.keyPressEvent(self, event)
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:

            if self.scene().focusItem():
                return

            command = CommandRemove(self.scene(), self.scene().selectedItems())
            self._undoStack.push(command)
            event.accept()
        elif event.matches(QtGui.QKeySequence.Copy):
            mime_data = self.copy_steps()
            QtWidgets.QApplication.clipboard().setMimeData(mime_data)
            event.accept()
        elif event.matches(QtGui.QKeySequence.Paste):
            if QtWidgets.QApplication.clipboard().mimeData().hasFormat('image/x-workflow-step(s)'):
                data = QtWidgets.QApplication.clipboard().mimeData().data("image/x-workflow-step(s)")
                stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
                self.paste_steps(stream)
                event.accept()
        else:
            event.ignore()

    def copy_steps(self, start_pos=QtCore.QPoint(0, 0)):
        """
        Generate and return a QMimeData object containing information for each of the current selected steps. This data is useful for
        copying and pasting steps within the MAP Client workflow area.

        When copying workflow items using the CTRL+Drag operation, you should specify a starting position. This argument is not necessary
        (or relavant) when copying items with the CTRL+C shortcut.
        """
        data = QtCore.QByteArray()
        data_stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)

        # The first part of the data_stream now gives the number of steps to be copied/pasted.
        data_stream.writeUInt32(len(self.scene().selectedItems()))
        data_stream << start_pos
        data_stream << QtCore.QPoint(0, 0)      # Hotspot

        for item in self.scene().selectedItems():
            if item.type() == Node.Type:
                name = item.metaItem().getStep().getName().encode('utf-8')
                data_stream.writeUInt32(len(name))
                buf = QtCore.QByteArray(name)
                data_stream << buf

                position = item.pos().toPoint()
                data_stream << position
            else:
                data_stream.writeUInt32(0)

                src_pos = item.sourceNode().parentItem().pos().toPoint()
                src_port_index = item.sourceNode().portIndex()
                dest_pos = item.destinationNode().parentItem().pos().toPoint()
                dest_port_index = item.destinationNode().portIndex()

                data_stream << src_pos
                data_stream.writeUInt32(src_port_index)
                data_stream << dest_pos
                data_stream.writeUInt32(dest_port_index)

        mime_data = QtCore.QMimeData()
        mime_data.setData('image/x-workflow-step(s)', data)
        return mime_data

    # TODO: Paste the arrows aswell.
    def paste_steps(self, stream, event_position=None):
        """
        This takes a stream of workflow items and pastes them to the workflow. See copy_steps for details on generating this stream.

        The optional parameter (event_position) can be used to specify where to paste the copied steps. This argument is not relavant
        when pasting workflow items using the CRTL+V shortcut, as this event has no position. In the future we may want to update the
        CTRL+V action to consider the last workflow position the user clicked and use this to generate an event_position argument.
        """
        scene = self.scene()
        start_pos = QtCore.QPoint()
        hotspot = QtCore.QPoint()
        position = QtCore.QPoint()
        buf = QtCore.QByteArray()
        arc_list = []

        self._undoStack.beginMacro('Paste Workflow Items')
        scene.clearSelection()

        item_count = stream.readUInt32()
        stream >> start_pos
        stream >> hotspot

        if event_position:
            offset = event_position - start_pos

        for _ in range(item_count):
            _name_len = stream.readUInt32()
            if _name_len == 0:
                src_pos = QtCore.QPoint()
                dest_pos = QtCore.QPoint()

                stream >> src_pos
                src_port_index = stream.readUInt32()
                stream >> dest_pos
                dest_port_index = stream.readUInt32()

                arc_list.append((src_pos, src_port_index, dest_pos, dest_port_index))
            else:
                stream >> buf
                stream >> position

                if event_position is None:
                    position.setX(position.x() + 20)
                    position.setY(position.y() + 20)
                else:
                    position = position + offset - hotspot

                name = buf.data().decode()
                node = self.create_node(scene, name)

                self._undoStack.push(CommandAdd(scene, node))
                self._undoStack.push(CommandMove(node, position, scene.ensureItemInScene(node, position)))

                node.setSelected(True)

        for arc in arc_list:
            src_pos, src_port_index = arc[0], arc[1]
            dest_pos, dest_port_index = arc[2], arc[3]

            if event_position is None:
                src_pos += QtCore.QPoint(20, 20)
                dest_pos += QtCore.QPoint(20, 20)
            else:
                src_pos = src_pos + offset - hotspot
                dest_pos = dest_pos + offset - hotspot

            src_port = self.scene().itemAt(self.mapToScene(src_pos), QtGui.QTransform())._step_port_items[src_port_index]
            dest_port = self.scene().itemAt(self.mapToScene(dest_pos), QtGui.QTransform())._step_port_items[dest_port_index]

            if (src_port and src_port.type() == StepPort.Type) and (dest_port and dest_port.type() == StepPort.Type):
                self.connectNodes(src_port, dest_port)

        self._undoStack.endMacro()
        self.setFocus()

    def setup_drag(self, start_pos):
        """
        Creates a QDrag object from the currently selected workflow items.

        Takes a starting position as an argument.
        """
        if len(self.scene().selectedItems()) > 1:
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(QtGui.QImage(':/workflow/images/clipboard_icon.png'))
        else:
            item = self.scene().itemAt(self.mapToScene(start_pos), QtGui.QTransform())
            step = item.metaItem().getStep()
            if step._icon:
                pixmap = QtGui.QPixmap(step._icon)
            else:
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(QtGui.QImage(':/workflow/images/default_step_icon.png'))

        pixmap = pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

        drag = QtGui.QDrag(self)
        drag.setMimeData(self.copy_steps(start_pos))
        drag.setHotSpot(hotspot)
        drag.setPixmap(pixmap)
        drag.exec_(QtCore.Qt.MoveAction)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.type() == Node.Type:
            item.showContextMenu(event.globalPos())

    def mousePressEvent(self, event):
        self._selectionStartPos = None
        item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
        if event.button() == QtCore.Qt.RightButton:
            event.ignore()
        elif item and item.type() == StepPort.Type:
            centre = item.boundingRect().center()
            self._connectSourceNode = item
            self._connectLine = ArrowLine(QtCore.QLineF(item.mapToScene(centre),
                                                        self.mapToScene(event.pos())))
            self.scene().addItem(self._connectLine)
        else:
            QtWidgets.QGraphicsView.mousePressEvent(self, event)
            self._selectionStartPos = event.pos()

    def mouseMoveEvent(self, event):
        if self._connectLine:
            newLine = QtCore.QLineF(self._connectLine.line().p1(), self.mapToScene(event.pos()))
            self._connectLine.setLine(newLine)
        else:
            QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

            # modifiers = QtWidgets.QApplication.keyboardModifiers()
            # if modifiers == QtCore.Qt.ControlModifier:
            #     self.setup_drag(event.pos())

    def mouseReleaseEvent(self, event):
        if self._connectLine:
            item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            if item and item.type() == StepPort.Type:
                self.connectNodes(self._connectSourceNode, item)
            self.scene().removeItem(self._connectLine)
            self._connectLine = None
            self._connectSourceNode = None
        else:
            QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
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
        if event.mimeData().hasFormat("image/x-workflow-step(s)"):
            piece_data = event.mimeData().data("image/x-workflow-step(s)")
            stream = QtCore.QDataStream(piece_data, QtCore.QIODevice.ReadOnly)
            self.paste_steps(stream, event.pos())
            event.accept()
        else:
            event.ignore()

    def create_node(self, scene, name):
        """
        Creates and returns a Node object based on the step name given.
        """
        # Create a step with the given name.
        step = workflowStepFactory(name, self._location)
        self.set_default_id(step)
        step.setMainWindow(self._main_window)
        step.setLocation(self._location)
        step.registerConfiguredObserver(scene.stepConfigured)
        step.registerDoneExecution(scene.doneExecution)
        step.registerOnExecuteEntry(scene.setCurrentWidget)
        step.registerIdentifierOccursCount(scene.identifierOccursCount)

        # Trigger a validation.
        step.deserialize(step.serialize())

        # Prepare meta step for the graphics scene.
        meta_step = MetaStep(step)
        node = Node(meta_step)
        node.showStepName(self._showStepNames)

        return node

    def set_default_id(self, step):
        # Check if there are any existing steps with the default identifier.
        scene = self.scene()

        no_space_name = step.getName().replace(" ", "_")
        potential_id = f'{no_space_name}'
        if scene.identifierOccursCount(potential_id):
            suffix = 1
            potential_id = f'{no_space_name}_{suffix}'
            while scene.identifierOccursCount(potential_id):
                suffix += 1
                potential_id = f'{no_space_name}_{suffix}'

        step.setIdentifier(potential_id)

    def dragMoveEvent(self, event):
        QtWidgets.QGraphicsView.dragMoveEvent(self, event)
        if event.mimeData().hasFormat("image/x-workflow-step(s)"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

        self.update()

    def dragEnterEvent(self, event):
        QtWidgets.QGraphicsView.dragEnterEvent(self, event)
        if event.mimeData().hasFormat("image/x-workflow-step(s)"):
            event.accept()
        else:
            event.ignore()

    def showEvent(self, event):
        self._graphics_shown = True

    def resizeEvent(self, event):
        QtWidgets.QGraphicsView.resizeEvent(self, event)
        if self._graphics_shown:

            scene = self.scene()
            event_size = event.size()
            view_rect = QtCore.QRectF(0, 0, event_size.width(), event_size.height())
            if not self._graphics_initialised:
                scene.setReady()
                self._graphics_initialised = True

            scene.setSceneRect(10, 10, (view_rect.width() - 20) / self._graphics_scale_factor, (view_rect.height() - 20) / self._graphics_scale_factor)

    def _unscale_view(self, scale_factor):
        self._graphics_scale_factor *= scale_factor
        scene = self.scene()
        rect = scene.sceneRect()
        rect.setWidth(rect.width() / scale_factor)
        rect.setHeight(rect.height() / scale_factor)
        scene.setSceneRect(rect)

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            scale_factor = math.pow(2.0, -event.delta() / 240.0)
            # original_transformation_anchor = self.transformationAnchor()
            # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
            self.scale(scale_factor, scale_factor)
            self._unscale_view(scale_factor)
            # self.setTransformationAnchor(original_transformation_anchor)
        else:
            super(WorkflowGraphicsView, self).wheelEvent(event)

    def zoomIn(self):
        self.scale(1.2, 1.2)

    def zoomOut(self):
        self.scale(1 / 1.2, 1 / 1.2)

    def _old_scale_view(self, scale_factor):
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        transformation_anchor = self.transformationAnchor()
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.scale(scale_factor, scale_factor)
        self.setTransformationAnchor(transformation_anchor)
