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
        status = super(WorkflowStepsFilter, self).filterAcceptsRow(source_row, source_parent)
        if source_parent.isValid() and status:
            return True
        elif not source_parent.isValid():
            index = self.sourceModel().index(source_row, 0, source_parent)
            row = 0
            index_child = self.sourceModel().index(row, 0, index)
            while index_child.isValid():
                if super(WorkflowStepsFilter, self).filterAcceptsRow(row, index_child):
                    return True
                # At this point the filter always accepts the the filter for the given row
                # So this code is never used.  Which to me seems a little odd, however it results
                # in an effect that is satisfactory.
                row += 1
                index_child = index_child.sibling(row, 0)

        return status


class WorkflowSteps(QtGui.QStandardItemModel):

    def __init__(self, manager, parent=None):
        super(WorkflowSteps, self).__init__(parent)
        self._manager = manager

    def reload(self):
        self.clear()
        self.setColumnCount(1)
        for step in WorkflowStepMountPoint.getPlugins(''):
            addStep(self, step)
