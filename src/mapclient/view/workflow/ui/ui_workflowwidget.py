# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/view/workflow/qt/workflowwidget.ui',
# licensing of 'src/mapclient/view/workflow/qt/workflowwidget.ui' applies.
#
# Created: Wed Jun 26 11:12:51 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_WorkflowWidget(object):
    def setupUi(self, WorkflowWidget):
        WorkflowWidget.setObjectName("WorkflowWidget")
        WorkflowWidget.resize(992, 697)
        WorkflowWidget.setWindowTitle("")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(WorkflowWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(WorkflowWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEditFilter.setText("")
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.stepTreeView = WorkflowStepTreeView(self.layoutWidget_2)
        self.stepTreeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.stepTreeView.setDragEnabled(True)
        self.stepTreeView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.stepTreeView.setIconSize(QtCore.QSize(64, 64))
        self.stepTreeView.setIndentation(0)
        self.stepTreeView.setRootIsDecorated(False)
        self.stepTreeView.setSortingEnabled(False)
        self.stepTreeView.setHeaderHidden(True)
        self.stepTreeView.setExpandsOnDoubleClick(False)
        self.stepTreeView.setObjectName("stepTreeView")
        self.verticalLayout_2.addWidget(self.stepTreeView)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = WorkflowGraphicsView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(900, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.executeButton = QtWidgets.QPushButton(self.layoutWidget)
        self.executeButton.setObjectName("executeButton")
        self.horizontalLayout.addWidget(self.executeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(WorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkflowWidget)
        WorkflowWidget.setTabOrder(self.graphicsView, self.lineEditFilter)
        WorkflowWidget.setTabOrder(self.lineEditFilter, self.executeButton)

    def retranslateUi(self, WorkflowWidget):
        self.lineEditFilter.setPlaceholderText(QtWidgets.QApplication.translate("WorkflowWidget", "Filter", None, -1))
        self.executeButton.setText(QtWidgets.QApplication.translate("WorkflowWidget", "E&xecute", None, -1))

from mapclient.view.workflow.workflowgraphicsview import WorkflowGraphicsView
from mapclient.view.workflow.workflowsteptreeview import WorkflowStepTreeView
