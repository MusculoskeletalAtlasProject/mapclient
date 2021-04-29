# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ports.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Ports(object):
    def setupUi(self, Ports):
        if not Ports.objectName():
            Ports.setObjectName(u"Ports")
        Ports.resize(400, 300)
        self.gridLayout = QGridLayout(Ports)
        self.gridLayout.setObjectName(u"gridLayout")
        self.addButton = QPushButton(Ports)
        self.addButton.setObjectName(u"addButton")

        self.gridLayout.addWidget(self.addButton, 0, 1, 1, 1)

        self.portTableWidget = QTableWidget(Ports)
        self.portTableWidget.setObjectName(u"portTableWidget")
        self.portTableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.portTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.portTableWidget, 0, 0, 3, 1)

        self.removeButton = QPushButton(Ports)
        self.removeButton.setObjectName(u"removeButton")

        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)


        self.retranslateUi(Ports)

        QMetaObject.connectSlotsByName(Ports)
    # setupUi

    def retranslateUi(self, Ports):
        Ports.setWindowTitle(QCoreApplication.translate("Ports", u"Form", None))
        self.addButton.setText(QCoreApplication.translate("Ports", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("Ports", u"Remove", None))
    # retranslateUi

