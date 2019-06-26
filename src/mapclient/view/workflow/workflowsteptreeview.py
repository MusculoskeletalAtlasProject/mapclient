"""
Created on Aug 18, 2015

@author: hsorby
"""
import sys

from PySide2 import QtCore, QtWidgets, QtGui


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


class WorkflowStepTreeView(QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(WorkflowStepTreeView, self).__init__(parent)
        self.setItemDelegate(HeaderDelegate())
        self.setMinimumWidth(250)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self._leftMouseButton = False

        self._makeConnections()

    def _makeConnections(self):
        self.clicked.connect(self._handleMouseClicked)
        self.pressed.connect(self._handleMousePress)

    def mouseDoubleClickEvent(self, event):
        return event.accept()

    def setFilterRegExp(self, reg_exp):
        self.model().setFilterRegExp(reg_exp)

    def _handleMousePress(self, index):
        self._leftMouseButton = int(QtWidgets.QApplication.mouseButtons()) == QtCore.Qt.LeftButton
        if index.parent().isValid() and self._leftMouseButton:
            itemData = QtCore.QByteArray()
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
            step = self.model().data(index, QtCore.Qt.UserRole + 1)
            if step._icon:
                pixmap = QtGui.QPixmap(step._icon)
            else:
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(QtGui.QImage(':/workflow/images/default_step_icon.png'))

            pixmap = pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
            hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

            name = step.getName().encode('utf-8')  # bytearray(step.getName(), sys.stdout.encoding)
            dataStream.writeUInt32(len(name))
            if sys.version_info < (3, 0):
                dataStream.writeRawData(name)
            else:
                buf = QtCore.QByteArray(name)
                dataStream << buf#.writeRawData(name)

            dataStream << hotspot

            mimeData = QtCore.QMimeData()
            mimeData.setData('image/x-workflow-step', itemData)

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(hotspot)
            drag.setPixmap(pixmap)

            drag.exec_(QtCore.Qt.MoveAction)

    def _handleMouseClicked(self, index):

        if not index.isValid():
            return

        if not self._leftMouseButton:
            return

        if not index.parent().isValid():
            self.setExpanded(index, not self.isExpanded(index))
