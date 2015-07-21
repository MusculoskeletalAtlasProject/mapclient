# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/workflowwidget.ui'
#
# Created: Wed Sep 10 15:58:22 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WorkflowWidget(object):
    def setupUi(self, WorkflowWidget):
        WorkflowWidget.setObjectName("WorkflowWidget")
        WorkflowWidget.resize(922, 646)
        WorkflowWidget.setWindowTitle("")
        self.gridLayout = QtGui.QGridLayout(WorkflowWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(WorkflowWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.stepTree = StepTree(self.splitter)
        self.stepTree.setObjectName("stepTree")
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
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(WorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkflowWidget)

    def retranslateUi(self, WorkflowWidget):
        self.executeButton.setText(QtGui.QApplication.translate("WorkflowWidget", "E&xecute", None, QtGui.QApplication.UnicodeUTF8))

from mapclient.view.workflow.steptree import StepTree
from mapclient.view.workflow.workflowgraphicsview import WorkflowGraphicsView
