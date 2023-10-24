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

from mapclient.core.workflow.workflowutils import revert_parameterised_position
from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.workflow.workflowscene import MetaStep
from mapclient.view.utils import is_light_mode
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
        self._graphics_initialised = False
        self._graphics_scale_factor = 1.0
        self._margin = 10

        self._undoStack = None
        self._location = ''
        self._showStepNames = True

        self._connectLine = None
        self._connectSourceNode = None
        self._connectPotentialTarget = None

        self._selectionStartPos = None

        self.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

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
        if event.key() == QtCore.Qt.Key.Key_Backspace or event.key() == QtCore.Qt.Key.Key_Delete:

            if self.scene().focusItem():
                return

            command = CommandRemove(self.scene(), self.scene().selectedItems())
            self._undoStack.push(command)
            event.accept()
        elif event.matches(QtGui.QKeySequence.StandardKey.Copy):
            mime_data = self.copy_steps()
            QtWidgets.QApplication.clipboard().setMimeData(mime_data)
            event.accept()
        elif event.matches(QtGui.QKeySequence.StandardKey.Paste):
            if QtWidgets.QApplication.clipboard().mimeData().hasFormat('image/x-workflow-step(s)'):
                data = QtWidgets.QApplication.clipboard().mimeData().data("image/x-workflow-step(s)")
                stream = QtCore.QDataStream(data, QtCore.QIODevice.OpenModeFlag.ReadOnly)
                self.paste_steps(stream)
                event.accept()
        else:
            event.ignore()

    def copy_steps(self, start_pos=QtCore.QPoint(0, 0)):
        """
        Generate and return a QMimeData object containing information for each of the current selected steps. This data is useful for
        copying and pasting steps within the MAP Client workflow area.

        When copying workflow items using the CTRL+Drag operation, you should specify a starting position. This argument is not necessary
        (or relevant) when copying items with the CTRL+C shortcut.
        """
        data = QtCore.QByteArray()
        data_stream = QtCore.QDataStream(data, QtCore.QIODevice.OpenModeFlag.WriteOnly)

        # The first part of the data_stream now gives the number of steps to be copied/pasted.
        data_stream.writeUInt32(len(self.scene().selectedItems()))
        data_stream << start_pos
        data_stream << QtCore.QPoint(0, 0)  # Hotspot

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

    def paste_steps(self, stream, event_position=None):
        """
        This takes a stream of workflow items and pastes them to the workflow. See copy_steps for details on generating this stream.

        The optional parameter (event_position) can be used to specify where to paste the copied steps. This argument is not relevant
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

        offset = None
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
                self._undoStack.push(CommandMove(node, position, scene.ensure_item_in_scene(node, position)))

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

        pixmap = pixmap.scaled(64, 64, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
        hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

        drag = QtGui.QDrag(self)
        drag.setMimeData(self.copy_steps(start_pos))
        drag.setHotSpot(hotspot)
        drag.setPixmap(pixmap)
        drag.exec(QtCore.Qt.DropAction.MoveAction)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.type() == Node.Type:
            item.showContextMenu(event.globalPos())

    def mousePressEvent(self, event):
        self._selectionStartPos = None
        item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
        if event.button() == QtCore.Qt.MouseButton.RightButton:
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
            item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            if item and item.type() == StepPort.Type:
                if self._connectSourceNode != item:
                    self._connectPotentialTarget = item
                    item.highlight(True)
            elif self._connectPotentialTarget:
                self._connectPotentialTarget.highlight(False)
                self._connectPotentialTarget = None

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
            if self._connectPotentialTarget:
                self._connectPotentialTarget.highlight(False)

            self._connectLine = None
            self._connectSourceNode = None
            self._connectPotentialTarget = None
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
        if event.type() == QtCore.QEvent.Type.EnabledChange:
            self.invalidateScene(self.sceneRect())

    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        shadow_colour = QtCore.Qt.GlobalColor.darkGray if is_light_mode() else QtCore.Qt.GlobalColor.gray
        rightShadow = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
            painter.fillRect(rightShadow, shadow_colour)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
            painter.fillRect(bottomShadow, shadow_colour)

        self._draw_grid(sceneRect, painter)

    def _draw_grid(self, scene_rect, painter):
        purple = '#3D2645'
        french_blue = '#0075C4'
        grid_colour = "lightblue" if is_light_mode() else french_blue
        self.grid_pen = QtGui.QPen(QtGui.QColor(grid_colour))
        painter.setPen(self.grid_pen)

        top = int(scene_rect.y())
        left = int(scene_rect.x())
        bottom = int(scene_rect.y() + scene_rect.height())
        right = int(scene_rect.x() + scene_rect.width())
        step = 10

        for y in range(top, bottom, step):
            painter.drawLine(left, y, right, y)
        for x in range(left, right, step):
            painter.drawLine(x, top, x, bottom)

        rect_colour = QtGui.QColor("black") if is_light_mode() else QtGui.QColor("white")
        painter.setPen(QtGui.QPen(rect_colour))
        painter.drawRect(scene_rect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step(s)"):
            piece_data = event.mimeData().data("image/x-workflow-step(s)")
            stream = QtCore.QDataStream(piece_data, QtCore.QIODevice.OpenModeFlag.ReadOnly)
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
            event.setDropAction(QtCore.Qt.DropAction.MoveAction)
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

    def resizeEvent(self, event):
        QtWidgets.QGraphicsView.resizeEvent(self, event)

        scene = self.scene()
        event_size = event.size()
        view_rect = QtCore.QRectF(0, 0, event_size.width(), event_size.height())
        if not self._graphics_initialised:
            scene.setReady()
            self._graphics_initialised = True

        scene.setSceneRect(
            self._margin / self._graphics_scale_factor,
            self._margin / self._graphics_scale_factor,
            (view_rect.width() - 2 * self._margin) / self._graphics_scale_factor,
            (view_rect.height() - 2 * self._margin) / self._graphics_scale_factor
        )
        self._reposition_steps()

    def _unscale_view(self, scale_factor):
        self._graphics_scale_factor *= scale_factor
        scene = self.scene()
        rect = scene.sceneRect()
        rect.setWidth(rect.width() / scale_factor)
        rect.setHeight(rect.height() / scale_factor)
        scene.setSceneRect(rect)

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self._zoom(event.angleDelta().y())
        else:
            super(WorkflowGraphicsView, self).wheelEvent(event)

    def zoom_in(self):
        self._zoom(-120)

    def zoom_out(self):
        self._zoom(120)

    def _zoom(self, delta):
        scale_factor = math.pow(2.0, -delta / 240.0)
        self.scale(scale_factor, scale_factor)
        self._unscale_view(scale_factor)
        self._reposition_steps()

    def reset_zoom(self):
        reverse_sf = 1 / self._graphics_scale_factor
        self.scale(reverse_sf, reverse_sf)
        self._unscale_view(reverse_sf)
        self._reposition_steps()

        self._graphics_scale_factor = 1.0
        self.resetTransform()

    def _reposition_steps(self):
        scene_rect = self.sceneRect()
        for item in self.items():
            if isinstance(item, Node):
                new_position = revert_parameterised_position(scene_rect, item.parameterised_pos(), item.offset())
                item.setPos(new_position, False)

    def merge_macros(self):
        # If the top-most macro is successfully merged, remove it from the undo stack.
        merged_macro = self._merge_macros()
        if merged_macro:
            merged_macro.setObsolete(True)
            self._undoStack.undo()

    def _merge_macros(self):
        # Attempt to merge the top-most macro on the undo stack into the previous macro.
        try:
            current_cmd = self._undoStack.command(self._undoStack.index() - 1)
            previous_cmd = self._undoStack.command(self._undoStack.index() - 2)
            if current_cmd and not current_cmd.childCount():
                return current_cmd
            if previous_cmd:
                assert (current_cmd.text() == previous_cmd.text())
                assert (current_cmd.childCount() == previous_cmd.childCount())
                for i in range(previous_cmd.childCount()):
                    assert (isinstance(current_cmd.child(i), CommandMove))
                    assert (isinstance(previous_cmd.child(i), CommandMove))
                    assert (previous_cmd.child(i).node() == current_cmd.child(i).node())
                for i in range(previous_cmd.childCount()):
                    previous_cmd.child(i).mergeWith(current_cmd.child(i))
                return current_cmd

        except AssertionError:
            return None

    def view_all(self):
        bounding_rect = self.nodes_bounding_rect()
        scene_rect = self.sceneRect()

        # This includes 50px of whitespace on each side of the workflow items. Subtract 68 to account for step-icon width.
        sf_x = 1
        if (bounding_rect.right()) > (scene_rect.right() - 116):
            sf_x = (scene_rect.right() - 116) / bounding_rect.right()
        sf_y = 1
        if bounding_rect.bottom() > (scene_rect.bottom() - 116):
            sf_y = (scene_rect.bottom() - 116) / bounding_rect.bottom()

        if sf_x != 1 or sf_y != 1:
            self.scale_workflow(sf_x, sf_y)

    def nodes_bounding_rect(self):
        point_array = [[], []]
        for item in self.items():
            if isinstance(item, Node):
                point_array[0].append(item.x())
                point_array[1].append(item.y())

        if point_array[0]:
            return QtCore.QRectF(
                QtCore.QPointF(min(point_array[0]), min(point_array[1])),
                QtCore.QPointF(max(point_array[0]), max(point_array[1]))
            )
        else:
            return QtCore.QRectF(0, 0, 0, 0)

    def scale_workflow(self, sf_x, sf_y):
        # Scale the workflow item positions. Add self._margin to account for subtracting the view border before scaling.
        self._undoStack.beginMacro('Move Step(s)')
        for item in self.items():
            if isinstance(item, Node):
                x = item.x()
                if sf_x != 1:
                    x = ((x - self._margin) * sf_x) + self._margin
                y = item.y()
                if sf_y != 1:
                    y = ((y - self._margin) * sf_y) + self._margin

                if x != item.x() or y != item.y():
                    self._undoStack.push(CommandMove(item, item.pos(), QtCore.QPointF(x, y)))
        self._undoStack.endMacro()
