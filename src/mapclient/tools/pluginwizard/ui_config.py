# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.resize(400, 300)
        self.gridLayout = QGridLayout(Config)
        self.gridLayout.setObjectName(u"gridLayout")
        self.addButton = QPushButton(Config)
        self.addButton.setObjectName(u"addButton")

        self.gridLayout.addWidget(self.addButton, 1, 1, 1, 1)

        self.configTableWidget = QTableWidget(Config)
        if (self.configTableWidget.columnCount() < 2):
            self.configTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.configTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.configTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.configTableWidget.setObjectName(u"configTableWidget")
        self.configTableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.configTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.configTableWidget, 1, 0, 3, 1)

        self.removeButton = QPushButton(Config)
        self.removeButton.setObjectName(u"removeButton")

        self.gridLayout.addWidget(self.removeButton, 2, 1, 1, 1)

        self.identifierCheckBox = QCheckBox(Config)
        self.identifierCheckBox.setObjectName(u"identifierCheckBox")

        self.gridLayout.addWidget(self.identifierCheckBox, 0, 0, 1, 1)


        self.retranslateUi(Config)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate("Config", u"Form", None))
        self.addButton.setText(QCoreApplication.translate("Config", u"Add", None))
        ___qtablewidgetitem = self.configTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Config", u"Label", None));
        ___qtablewidgetitem1 = self.configTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Config", u"Default Value", None));
        self.removeButton.setText(QCoreApplication.translate("Config", u"Remove", None))
        self.identifierCheckBox.setText(QCoreApplication.translate("Config", u"Define 'Identifier' configuration value", None))
    # retranslateUi

