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
from PySide2 import QtCore, QtGui, QtWidgets


class HeaderDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(HeaderDelegate, self).__init__(parent)
        self._arrow_right = QtGui.QPixmap(':/mapclient/images/icon-arrow-right.png')
        trans = QtGui.QTransform()
        trans.rotate(90.0)
        self._arrow_down = self._arrow_right.transformed(trans)

    def paint(self, painter, option, index):
        if index.parent().row() < 0:
            rx = option.rect.x()
            ry = option.rect.y()
            ht = option.rect.height()
            wd = option.rect.width()
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            painter.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
            painter.drawRoundedRect(rx + 1, ry + 1, wd - 2, ht - 2, 7, 7, QtCore.Qt.RelativeSize)

            if option.state & QtWidgets.QStyle.State_Open:
                required_arrow = self._arrow_down
            else:
                required_arrow = self._arrow_right

            painter.drawPixmap(rx + 3, ry + 3, ht - 6, ht - 6, required_arrow)
            painter.drawText(option.rect, index.data(), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            super(HeaderDelegate, self).paint(painter, option, index)


class StepTree(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(StepTree, self).__init__(parent)
        self.setItemDelegate(HeaderDelegate())

        self.stepIconSize = 64
        size = QtCore.QSize(self.stepIconSize, self.stepIconSize)
        self.setIconSize(size)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setIndentation(0)

        self.itemClicked.connect(self.handleMouseClicked)
        self.itemPressed.connect(self.handleMousePress)
        self._leftMouseButton = False

        self.setMinimumWidth(250)

    def mouseDoubleClickEvent(self, event):
        return event.accept()

    def handleMousePress(self, event):
        self._leftMouseButton = int(QtGui.QGuiApplication.mouseButtons()) == QtCore.Qt.LeftButton

    def handleMouseClicked(self, item):

        if item is None:
            return

        if not self._leftMouseButton:
            return

        if item.parent() is None:
            self.setItemExpanded(item, not self.isItemExpanded(item))
            return

    def findParentItem(self, category):
        parentItem = None
        for index in range(self.topLevelItemCount()):
            item = self.topLevelItem(index)
            if item.text(0) == category:
                parentItem = item
                break

        return parentItem

    def addStep(self, step):

        column = 0
        parentItem = self.findParentItem(step._category)
        if not parentItem:
            parentItem = QtWidgets.QTreeWidgetItem(self)
            parentItem.setText(column, step._category)
            parentItem.setTextAlignment(column, QtCore.Qt.AlignCenter)
            font = parentItem.font(column)
            font.setPointSize(12)
            font.setWeight(QtGui.QFont.Bold)
            parentItem.setFont(column, font)

        if not parentItem.isExpanded():
            parentItem.setExpanded(True)

        stepItem = QtWidgets.QTreeWidgetItem(parentItem)
        stepItem.setText(column, step.getName())
        if step._icon:
            stepItem.setIcon(column, QtGui.QIcon(QtGui.QPixmap.fromImage(step._icon)))
        else:
            stepItem.setIcon(column, QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(':/workflow/images/default_step_icon.png'))))

        stepItem.setData(column, QtCore.Qt.UserRole, step)
        stepItem.setFlags(QtCore.Qt.ItemIsEnabled)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return None

        if self.indexOfTopLevelItem(item) >= 0:
            # Item is a top level item and it doesn't have drag and drop abilities
            return QtWidgets.QTreeWidget.mousePressEvent(self, event)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        step = item.data(0, QtCore.Qt.UserRole)
        if step._icon:
            pixmap = QtGui.QPixmap(step._icon)
        else:
            # icon = createDefaultImageIcon(step.getName())
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(QtGui.QImage(':/workflow/images/default_step_icon.png'))

        pixmap = pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

        name = step.getName().encode('utf-8')  # bytearray(step.getName(), sys.stdout.encoding)
        dataStream.writeUInt32(len(name))
        dataStream.writeRawData(name)

        dataStream << hotspot

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-workflow-step', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(hotspot)
        drag.setPixmap(pixmap)

        drag.exec_(QtCore.Qt.MoveAction)

        return QtWidgets.QTreeWidget.mousePressEvent(self, event)
