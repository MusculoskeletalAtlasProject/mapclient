# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'workflowwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mapclient.view.workflow.workflowgraphicsview import WorkflowGraphicsView
from mapclient.view.workflow.workflowsteptreeview import WorkflowStepTreeView


class Ui_WorkflowWidget(object):
    def setupUi(self, WorkflowWidget):
        if not WorkflowWidget.objectName():
            WorkflowWidget.setObjectName(u"WorkflowWidget")
        WorkflowWidget.resize(1009, 697)
        self.verticalLayout_3 = QVBoxLayout(WorkflowWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(WorkflowWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEditFilter = QLineEdit(self.layoutWidget_2)
        self.lineEditFilter.setObjectName(u"lineEditFilter")

        self.verticalLayout_2.addWidget(self.lineEditFilter)

        self.stepTreeView = WorkflowStepTreeView(self.layoutWidget_2)
        self.stepTreeView.setObjectName(u"stepTreeView")
        self.stepTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stepTreeView.setDragEnabled(True)
        self.stepTreeView.setSelectionMode(QAbstractItemView.NoSelection)
        self.stepTreeView.setIconSize(QSize(64, 64))
        self.stepTreeView.setIndentation(0)
        self.stepTreeView.setRootIsDecorated(False)
        self.stepTreeView.setSortingEnabled(False)
        self.stepTreeView.setHeaderHidden(True)
        self.stepTreeView.setExpandsOnDoubleClick(False)

        self.verticalLayout_2.addWidget(self.stepTreeView)

        self.splitter.addWidget(self.layoutWidget_2)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = WorkflowGraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QSize(900, 600))
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.verticalLayout.addWidget(self.graphicsView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.executeButton = QPushButton(self.layoutWidget)
        self.executeButton.setObjectName(u"executeButton")

        self.horizontalLayout.addWidget(self.executeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.layoutWidget)

        self.verticalLayout_3.addWidget(self.splitter)

        QWidget.setTabOrder(self.graphicsView, self.lineEditFilter)
        QWidget.setTabOrder(self.lineEditFilter, self.executeButton)

        self.retranslateUi(WorkflowWidget)

        QMetaObject.connectSlotsByName(WorkflowWidget)
    # setupUi

    def retranslateUi(self, WorkflowWidget):
        WorkflowWidget.setWindowTitle("")
        self.lineEditFilter.setText("")
        self.lineEditFilter.setPlaceholderText(QCoreApplication.translate("WorkflowWidget", u"Filter", None))
        self.executeButton.setText(QCoreApplication.translate("WorkflowWidget", u"E&xecute", None))
    # retranslateUi

