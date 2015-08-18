# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/workflowwidget.ui'
#
# Created: Tue Aug 18 17:22:36 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WorkflowWidget(object):
    def setupUi(self, WorkflowWidget):
        WorkflowWidget.setObjectName("WorkflowWidget")
        WorkflowWidget.resize(992, 697)
        WorkflowWidget.setWindowTitle("")
        self.verticalLayout_3 = QtGui.QVBoxLayout(WorkflowWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtGui.QSplitter(WorkflowWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtGui.QLineEdit(self.layoutWidget_2)
        self.lineEditFilter.setText("")
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.stepTreeView = WorkflowStepTreeView(self.layoutWidget_2)
        self.stepTreeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.stepTreeView.setDragEnabled(True)
        self.stepTreeView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.stepTreeView.setIconSize(QtCore.QSize(64, 64))
        self.stepTreeView.setIndentation(0)
        self.stepTreeView.setRootIsDecorated(False)
        self.stepTreeView.setSortingEnabled(True)
        self.stepTreeView.setHeaderHidden(True)
        self.stepTreeView.setExpandsOnDoubleClick(True)
        self.stepTreeView.setObjectName("stepTreeView")
        self.verticalLayout_2.addWidget(self.stepTreeView)
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = WorkflowGraphicsView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(900, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.executeButton = QtGui.QPushButton(self.layoutWidget)
        self.executeButton.setObjectName("executeButton")
        self.horizontalLayout.addWidget(self.executeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(WorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkflowWidget)
        WorkflowWidget.setTabOrder(self.graphicsView, self.lineEditFilter)
        WorkflowWidget.setTabOrder(self.lineEditFilter, self.executeButton)

    def retranslateUi(self, WorkflowWidget):
        self.lineEditFilter.setPlaceholderText(QtGui.QApplication.translate("WorkflowWidget", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.executeButton.setText(QtGui.QApplication.translate("WorkflowWidget", "E&xecute", None, QtGui.QApplication.UnicodeUTF8))

from mapclient.view.workflow.workflowgraphicsview import WorkflowGraphicsView
from mapclient.view.workflow.workflowsteptreeview import WorkflowStepTreeView
