"""
Created on Aug 18, 2015

@author: hsorby
"""
from PySide6 import QtCore, QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint


def addStep(model, step):
    category = step.getCategory()
    items = model.findItems(category)

    if not items:
        rootItem = model.invisibleRootItem()
        parentItem = QtGui.QStandardItem()
        parentItem.setText(category)
        font = parentItem.font()
        font.setPointSize(12)
        font.setWeight(QtGui.QFont.Bold)
        parentItem.setFont(font)
        rootItem.appendRow(parentItem)
    else:
        parentItem = items[0]

    item = QtGui.QStandardItem()
    item.setData(step)
    icon = step.getIcon()
    if icon:
        item.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(icon)))
    else:
        item.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(':/workflow/images/default_step_icon.png'))))

    item.setData(step.getName(), QtCore.Qt.DisplayRole)
    parentItem.appendRow(item)


class WorkflowStepsFilter(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(WorkflowStepsFilter, self).__init__(parent)

    def filterAcceptsRow(self, source_row, source_parent):
        # Categories are always shown, only steps are filtered.
        if not source_parent.isValid():
            return True

        return super(WorkflowStepsFilter, self).filterAcceptsRow(source_row, source_parent)


class WorkflowSteps(QtGui.QStandardItemModel):

    def __init__(self, manager, parent=None):
        super(WorkflowSteps, self).__init__(parent)
        self._manager = manager

    def reload(self):
        self.clear()
        self.setColumnCount(1)
        for step in WorkflowStepMountPoint.get_all_plugins(''):
            addStep(self, step)
