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
import math
import weakref

from PySide6 import QtCore, QtWidgets, QtGui

from mapclient.core.annotations import PROVIDES_ANNOTATIONS, USES_ANNOTATIONS, ANNOTATION_BASE
from mapclient.core.workflow.workflowscene import Connection
from mapclient.core.workflow.workflowutils import convert_to_parameterised_position
from mapclient.tools.annotation.annotationdialog import AnnotationDialog
from mapclient.tools.pmr.pmrdvcshelper import repositoryIsUpToDate
from mapclient.view.utils import is_light_mode


def _define_tooltip_for_triples(triples):
    tips = []
    for triple in triples:
        stub = triple[1].replace(ANNOTATION_BASE, '')
        tips.append(f'{stub}: {triple[2]}')

    return '\n or\n'.join(tips)


class ErrorItem(QtWidgets.QGraphicsItem):

    def __init__(self, sourceNode, destNode):
        QtWidgets.QGraphicsItem.__init__(self)
        self._source = weakref.ref(sourceNode)
        self._dest = weakref.ref(destNode)
        self._sourcePoint = QtCore.QPointF()
        self._destPoint = QtCore.QPointF()
        self._pixmap = QtGui.QPixmap(':/workflow/images/cancel_256.png').scaled(16, 16, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
        self._source().addArc(self)
        self._dest().addArc(self)
        self.setZValue(-1.5)
        self.adjust()
        # if hasattr(sourceNode, '_step_port_items'):
        #     print(sourceNode._step_port_items)

    def boundingRect(self):
        extra = (16) / 2.0  # Icon size divided by two

        return QtCore.QRectF(self._sourcePoint,
                             QtCore.QSizeF(self._destPoint.x() - self._sourcePoint.x(),
                                           self._destPoint.y() - self._sourcePoint.y())).normalized().adjusted(-extra,
                                                                                                               -extra,
                                                                                                               extra,
                                                                                                               extra)

    def adjust(self):
        if not self._source() or not self._dest():
            return

        sourceCentre = self._source().boundingRect().center()
        destCentre = self._dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self._source(), sourceCentre.x(), sourceCentre.y()),
                             self.mapFromItem(self._dest(), destCentre.x(), destCentre.y()))
        length = line.length()

        if length == 0.0:
            return

        arcOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self._sourcePoint = line.p1() + arcOffset
        self._destPoint = line.p2() - arcOffset

    def paint(self, painter, option, widget=None):
        midPoint = (self._destPoint + self._sourcePoint) / 2
        # Draw the line itself.
        line = QtCore.QLineF(self._sourcePoint, self._destPoint)

        if line.length() == 0.0:
            return

        brush_colour = QtCore.Qt.GlobalColor.black if is_light_mode() else QtCore.Qt.GlobalColor.gray
        painter.setPen(QtGui.QPen(brush_colour, 1, QtCore.Qt.PenStyle.DashLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(line)

        painter.drawPixmap(midPoint.x() - 8, midPoint.y() - 8, self._pixmap)


class Item(QtWidgets.QGraphicsItem):
    """
    Class to contain the selection information that selectable scene items can be derived from.
    """

    def __init__(self):
        QtWidgets.QGraphicsItem.__init__(self)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self._brush_colour = QtCore.Qt.GlobalColor.black if is_light_mode() else QtCore.Qt.GlobalColor.gray

    def setSelected(self, selected):
        QtWidgets.QGraphicsItem.setSelected(self, selected)
        self.scene().workflowScene().setItemSelected(self.metaItem(), selected)


class Arc(Item):
    """
    This class represents a connection between two ports.
    """
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtWidgets.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        Item.__init__(self)
        self.setAcceptHoverEvents(True)

        self._arrowSize = 10.0
        self._arrow = QtGui.QPolygonF()
        self._highlight = False

        self._connection = Connection(sourceNode.parentItem()._metastep, sourceNode.portIndex(),
                                      destNode.parentItem()._metastep, destNode.portIndex())
        self._connection.setSelected(False)

        self._sourcePoint = QtCore.QPointF()
        self._destPoint = QtCore.QPointF()
        #        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self._source = weakref.ref(sourceNode)
        self._dest = weakref.ref(destNode)
        self._source().addArc(self)
        self._dest().addArc(self)
        self.setZValue(-2.0)
        self.adjust()

    def type(self):
        return Arc.Type

    def hoverEnterEvent(self, event):
        self._highlight = True
        self.update()

    def hoverLeaveEvent(self, event):
        self._highlight = False
        self.update()

    def metaItem(self):
        return self._connection

    def sourceNode(self):
        return self._source()

    def destinationNode(self):
        return self._dest()

    def adjust(self):
        if not self._source() or not self._dest():
            return

        sourceCentre = self._source().boundingRect().center()
        destinationCentre = self._dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self._source(), sourceCentre.x(), sourceCentre.y()),
                             self.mapFromItem(self._dest(), destinationCentre.x(), destinationCentre.y()))
        length = line.length()

        if length == 0.0:
            return

        arcOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)
        self.prepareGeometryChange()
        self._sourcePoint = line.p1() + arcOffset
        self._destPoint = line.p2() - arcOffset

    def shape(self):
        path = QtGui.QPainterPath()
        path.addPolygon(self._arrow)
        return path

    def boundingRect(self):
        if not self._source() or not self._dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self._arrowSize) / 2.0

        sceneRect = QtCore.QRectF(self._sourcePoint,
                                  QtCore.QSizeF(self._destPoint.x() - self._sourcePoint.x(),
                                                self._destPoint.y() - self._sourcePoint.y())) \
            .normalized().adjusted(-extra, -extra, extra, extra)

        return sceneRect

    def paint(self, painter, option, widget=None):
        if not self._source() or not self._dest():
            return

        # Draw the line itself.
        line = QtCore.QLineF(self._sourcePoint, self._destPoint)

        if line.length() == 0.0:
            return

        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:  # or self.selected:
            painter.setBrush(QtCore.Qt.GlobalColor.darkGray)
            painter.drawRoundedRect(self.boundingRect(), 5, 5)

        brush = QtGui.QBrush(self._brush_colour)
        painter.setBrush(brush)

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Arc.TwoPi - angle

        # Draw the arrows if there's enough room.
        if line.dy() * line.dy() + line.dx() * line.dx() > 200 * self._arrowSize:
            midPoint = QtCore.QPointF((self._destPoint + self._sourcePoint) / 2)

            destination_arrow_p1 = midPoint + QtCore.QPointF(math.sin(angle - Arc.Pi / 3) * self._arrowSize,
                                                             math.cos(angle - Arc.Pi / 3) * self._arrowSize)
            destination_arrow_p2 = midPoint + QtCore.QPointF(math.sin(angle - Arc.Pi + Arc.Pi / 3) * self._arrowSize,
                                                             math.cos(angle - Arc.Pi + Arc.Pi / 3) * self._arrowSize)

            self._arrow.clear()
            self._arrow.append(midPoint)
            self._arrow.append(destination_arrow_p1)
            self._arrow.append(destination_arrow_p2)
            if self._highlight:
                painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.yellow, 2))
            painter.drawPolygon(self._arrow)

        painter.setPen(QtGui.QPen(brush, 1, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin))
        # painter.setPen(QtGui.QPen(QtCore.Qt.SolidLine))
        painter.drawLine(line)


class Node(Item):
    """
    This class is a graphical representation of the step on the canvas or in the step box.
    """
    Type = QtWidgets.QGraphicsItem.UserType + 1
    Size = 64

    def __init__(self, metastep):
        Item.__init__(self)

        self._margin = 2.0
        self._metastep = metastep
        icon = self._metastep.getStep().getIcon()
        if not icon:
            icon = QtGui.QImage(':/workflow/images/default_step_icon.png')

        self._pixmap = QtGui.QPixmap.fromImage(icon) \
            .scaled(self.Size, self.Size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)

        self._step_port_items = []
        self._parameterised_pos = QtCore.QPointF(0, 0)
        self._text = StepText(metastep.getStep().getName(), self)
        self._updateTextIcon()

        self._setToolTip()

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(self.CacheMode.DeviceCoordinateCache)
        self.setZValue(-1)

        self._contextMenu = QtWidgets.QMenu()
        configureAction = QtGui.QAction('Configure', self._contextMenu)
        configureAction.triggered.connect(self.configureMe)
        annotateAction = QtGui.QAction('Annotate', self._contextMenu)
        annotateAction.setEnabled(False)
        annotateAction.triggered.connect(self.annotateMe)
        deleteAction = QtGui.QAction('Delete', self._contextMenu)
        deleteAction.triggered.connect(self._removeMe)
        self._contextMenu.addAction(configureAction)
        self._contextMenu.addAction(annotateAction)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(deleteAction)

        self._updatePorts()

        self._configure_item = ConfigureIcon(self)
        self._configure_item.moveBy(40, 40)

        self._updateConfigureIcon()

        self._modified_item = MercurialIcon(self)
        self._modified_item.moveBy(5, 40)

        self.updateDVCSIcon()

    def update(self):
        self._updateConfigureIcon()
        self._updatePorts()
        self._updateTextIcon()
        super(Node, self).update()

    def _updateTextIcon(self):
        # Set text position
        br = self._text.boundingRect()
        x_pos = self.Size / 2 - br.width() / 2
        y_pos = self.Size + 5
        self._text.setPos(x_pos, y_pos)

    def _updateConfigureIcon(self):
        self._configure_item.setConfigured(self._metastep.getStep().isConfigured())
        self._setToolTip()

    def _setToolTip(self):
        self.setToolTip(self._metastep._step.getName() + ": " + self._metastep._step.getIdentifier())
        self._text.setText(
            self._metastep.getStepIdentifier() if self._metastep.getStepIdentifier() != self._metastep.getUniqueIdentifier() else self._metastep.getName())
        self._updateTextIcon()

    def _updatePorts(self):
        previous_step_ports = {}
        current_step_ports = self._metastep._step._ports
        for p in self._step_port_items:
            previous_step_ports[p.port()] = p

        self._step_port_items = []
        # Collect all ports that provide or use from the step
        uses_ports = [port for port in current_step_ports if port.hasUses()]
        provides_ports = [port for port in current_step_ports if port.hasProvides()]

        uses_count = 0
        uses_total = len(uses_ports)
        provides_count = 0
        provides_total = len(provides_ports)
        for port in current_step_ports:
            if port in previous_step_ports:
                port_item = previous_step_ports[port]
                del previous_step_ports[port]
            else:
                port_item = StepPort(port, self)
            w = port_item.width()
            h = port_item.height()
            if port in uses_ports:
                port_total = uses_total
                index = uses_count
                x_pos = -3 * w / 4
                uses_count += 1
                predicates = USES_ANNOTATIONS
            else:  # port in provides_ports:
                port_total = provides_total
                index = provides_count
                x_pos = self.Size - w / 4
                provides_count += 1
                predicates = PROVIDES_ANNOTATIONS

            triples = []
            for predicate in predicates:
                triples.extend(port.getTriplesForPred(predicate))
            # triple_objects = [triple[2] for triple in triples]

            alpha = h / 4.0  # Controls the spacing between the ports
            y_pos = self.Size / 2.0 - (port_total * h + (port_total - 1) * alpha) / 2.0 + (h + alpha) * index
            port_item.setPos(x_pos, y_pos)
            port_item.setToolTip(_define_tooltip_for_triples(triples))
            self._step_port_items.append(port_item)

        for port in previous_step_ports:
            old_port = previous_step_ports[port]
            old_port.setParentItem(None)

    def updateDVCSIcon(self):
        """
        :TODO: Update this for setting/saving output/input for step to repository
        """
        if self._metastep.getStep().getIdentifier():
            if repositoryIsUpToDate(self._getStepLocation()):
                self._modified_item.hide()
            else:
                self._modified_item.show()
        else:
            self._modified_item.hide()

    def setPos(self, pos, modify_parameterised=True):
        super(Node, self).setPos(pos)
        scene = self.scene()
        if modify_parameterised:
            self._parameterised_pos = convert_to_parameterised_position(scene.sceneRect(), pos, self.offset())
        self._metastep.setPos(pos)

    def set_parameterised_pos(self, parameterised_pos):
        self._parameterised_pos = parameterised_pos

    def parameterised_pos(self):
        return self._parameterised_pos

    def type(self):
        return Node.Type

    def commitMe(self):
        """
        :TODO: Update this for setting/saving data to repository
        """
        step_location = self._getStepLocation()
        if not repositoryIsUpToDate(step_location):
            self.scene().commitChanges(step_location)
            self.updateDVCSIcon()

    def _removeMe(self):
        self.scene().removeStep(self)

    def configureMe(self):
        self.scene().setConfigureNode(self)
        self._metastep._step.configure()

    def getConfig(self):
        return self._metastep._step.serialize()

    def setConfig(self, config):
        self._metastep._step.deserialize(config)

    def annotateMe(self):
        dlg = AnnotationDialog(self._getStepLocation())
        dlg.setModal(True)
        dlg.exec()

    def showStepName(self, show):
        self._text.setVisible(show)

    def metaItem(self):
        return self._metastep

    def offset(self):
        return QtCore.QPointF(self._pixmap.width(), self._pixmap.height())

    def boundingRect(self):
        return QtCore.QRectF(-self._margin, -self._margin,
                             self._pixmap.width() + 2 * self._margin,
                             self._pixmap.height() + 2 * self._margin)

    def paint(self, painter, option, widget=None):
        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:  # or self.selected:
            painter.setBrush(QtCore.Qt.GlobalColor.darkGray)
            painter.drawRoundedRect(self.boundingRect(), 5, 5)

        #            super(Node, self).paint(painter, option, widget)
        painter.drawPixmap(0, 0, self._pixmap)

    #            if not self._metastep._step.isConfigured():
    #                painter.drawPixmap(40, 40, self._configure_red)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.scene():
            return self.scene().ensure_item_in_scene(self, value)
        elif change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for port_item in self._step_port_items:
                port_item.itemChange(change, value)

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    def showContextMenu(self, pos):
        has_dir = os.path.exists(self._getStepLocation())
        self._contextMenu.actions()[1].setEnabled(has_dir)
        self._contextMenu.popup(pos)

    def _getStepLocation(self):
        return os.path.join(self._metastep._step._location, self._metastep._step.getIdentifier())


class StepPort(QtWidgets.QGraphicsEllipseItem):
    Type = QtWidgets.QGraphicsItem.UserType + 3

    def __init__(self, port, parent):
        super().__init__(0, 0, 11, 11, parent=parent)
        self._port = port
        self._connections = []
        self.setAcceptHoverEvents(True)
        self._highlight = False
        self._pixmap = QtGui.QPixmap(':/workflow/images/icon-port.png')
        # .scaled(11, 11, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

    def hoverEnterEvent(self, event):
        self._highlight = True
        self.update()

    def hoverLeaveEvent(self, event):
        self._highlight = False
        self.update()

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(0, 0, self._pixmap)
        if self._highlight:
            painter.setPen(QtCore.Qt.GlobalColor.yellow)
            painter.drawRoundedRect(self.boundingRect(), 5, 5)

    def type(self):
        return StepPort.Type

    def highlight(self, state):
        self._highlight = state
        self.update()

    def connections(self):
        return self._connections

    def port(self):
        return self._port

    def portIndex(self):
        return self._port.index()

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()

    def canConnect(self, other):
        if other.hasConnections():
            return False

        return self._port.canConnect(other._port)

    def hasConnections(self):
        self._removeDeadwood()
        return len(self._connections) > 0

    def _removeDeadwood(self):
        """
        Unfortunately the weakref doesn't work correctly for c based classes.  This function
        removes any None type references in _connections.
        """
        prunedArcList = [arc for arc in self._connections if arc()]
        self._connections = prunedArcList

    def hasArcToDestination(self, node):
        self._removeDeadwood()
        for arc in self._connections:
            if arc()._dest() == node:
                return True

        return False

    def addArc(self, arc):
        if not weakref.ref(arc) in self._connections:
            self._connections.append(weakref.ref(arc))

    def removeArc(self, arc):
        self._connections = [weakarc for weakarc in self._connections if weakarc() != arc]

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self._removeDeadwood()
            for arc in self._connections:
                arc().adjust()

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)


class StepText(QtWidgets.QGraphicsTextItem):
    Type = QtWidgets.QGraphicsItem.UserType + 4

    def __init__(self, *args):
        super().__init__(*args)
        self._editable_flags = QtCore.Qt.TextInteractionFlag.TextEditable | QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard
        self.setTextInteractionFlags(self._editable_flags)
        self._active_key = None
        self._make_connections()

    def _make_connections(self):
        self.document().contentsChanged.connect(self.adjust)

    def _update_identifier(self):
        self.scene().setConfigureNode(self.parentItem())
        step = self.parentItem().metaItem().getStep()
        step.setIdentifier(self.toPlainText())
        step._configuredObserver()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._update_identifier()

    def mousePressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.NoModifier:
            self.setTextInteractionFlags(self._editable_flags)
        else:
            self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        self._active_key = event.key()
        if self._active_key != QtCore.Qt.Key.Key_Return and self._active_key != QtCore.Qt.Key.Key_Enter:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if self._active_key and self._active_key == event.key():
            if self._active_key == QtCore.Qt.Key.Key_Return or self._active_key == QtCore.Qt.Key.Key_Enter:
                self._update_identifier()
                self.clearFocus()
                self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)

        self._active_key = None

    def adjust(self):
        parent_x = self.parentItem().boundingRect().center().x()
        offset = int(self.boundingRect().width() / 2)
        self.setX(parent_x - offset)

    def setText(self, text):
        self.setPlainText(text)

    def paint(self, painter, option, widget=None):
        painter.eraseRect(self.boundingRect())
        # painter.setBrush(QtCore.Qt.white)
        painter.drawRoundedRect(self.boundingRect(), 5, 5)
        super(StepText, self).paint(painter, option, widget)


class MercurialIcon(QtWidgets.QGraphicsItem):

    def __init__(self, *args, **kwargs):
        super(MercurialIcon, self).__init__(*args, **kwargs)
        self._hg_yellow = QtGui.QPixmap(':/workflow/images/modified_repo.png') \
            .scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
        self.setToolTip('The repository has been modified')
        self._highlight = False

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(0, 0, self._hg_yellow)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 24, 24)

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.scene().itemAt(event.scenePos()) == self:
            self.parentItem().commitMe()


class ConfigureIcon(QtWidgets.QGraphicsItem):

    def __init__(self, *args, **kwargs):
        super(ConfigureIcon, self).__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self._highlight = False
        self._configured = False
        self._configure_green = QtGui.QPixmap(':/workflow/images/configure_green.png').scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
        self._configure_red = QtGui.QPixmap(':/workflow/images/configure_red.png').scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
        self.setToolTip('Configure the step')

    def setConfigured(self, state):
        self._configured = state

    def hoverEnterEvent(self, event):
        self._highlight = True
        self.update()

    def hoverLeaveEvent(self, event):
        self._highlight = False
        self.update()

    def paint(self, painter, option, widget=None):
        pixmap = self._configure_red
        if self._configured:
            pixmap = self._configure_green

        painter.drawPixmap(0, 0, pixmap)
        if self._highlight:
            painter.setPen(QtCore.Qt.GlobalColor.yellow)
            painter.drawRoundedRect(self.boundingRect(), 12, 12)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 24, 24)

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.scene().itemAt(event.scenePos(), QtGui.QTransform()) == self:
            self.parentItem().configureMe()


class ArrowLine(QtWidgets.QGraphicsLineItem):

    def __init__(self, *args, **kwargs):
        super(ArrowLine, self).__init__(*args, **kwargs)
        self._arrowSize = 10.0
        self.setZValue(-2.0)
        self._brush_colour = QtCore.Qt.GlobalColor.black if is_light_mode() else QtCore.Qt.GlobalColor.gray
        self.setPen(QtGui.QPen(self._brush_colour, 1, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin))

    def boundingRect(self):
        penWidth = 1
        extra = (penWidth + self._arrowSize) / 2.0
        line = self.line()
        return QtCore.QRectF(line.p1(),
                             QtCore.QSizeF(line.p2().x() - line.p1().x(),
                                           line.p2().y() - line.p1().y())).normalized().adjusted(-extra, -extra, extra,
                                                                                                 extra)

    def paint(self, painter, option, widget=None):
        super(ArrowLine, self).paint(painter, option, widget)

        line = self.line()
        if line.length() == 0:
            return

        angle = math.acos(line.dx() / line.length())
        #        print('angle: ', angle)
        if line.dy() >= 0:
            angle = Arc.TwoPi - angle
        # Draw the arrows if there's enough room.
        if line.dy() * line.dy() + line.dx() * line.dx() > 200 * self._arrowSize:
            midPoint = QtCore.QPointF((line.p1() + line.p2()) / 2)

            destination_arrow_p1 = midPoint + QtCore.QPointF(math.sin(angle - Arc.Pi / 3) * self._arrowSize,
                                                             math.cos(angle - Arc.Pi / 3) * self._arrowSize)
            destination_arrow_p2 = midPoint + QtCore.QPointF(math.sin(angle - Arc.Pi + Arc.Pi / 3) * self._arrowSize,
                                                             math.cos(angle - Arc.Pi + Arc.Pi / 3) * self._arrowSize)

            painter.setBrush(self._brush_colour)
            painter.drawPolygon(QtGui.QPolygonF([midPoint, destination_arrow_p1, destination_arrow_p2]))
