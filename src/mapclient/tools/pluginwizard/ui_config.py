# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/config.ui'
#
# Created: Wed Oct 23 16:46:36 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Config(object):
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Config)
        self.gridLayout.setObjectName("gridLayout")
        self.addButton = QtGui.QPushButton(Config)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 1, 1, 1, 1)
        self.configTableWidget = QtGui.QTableWidget(Config)
        self.configTableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.configTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.configTableWidget.setObjectName("configTableWidget")
        self.configTableWidget.setColumnCount(2)
        self.configTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.configTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.configTableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.configTableWidget, 1, 0, 3, 1)
        self.removeButton = QtGui.QPushButton(Config)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 2, 1, 1, 1)
        self.identifierCheckBox = QtGui.QCheckBox(Config)
        self.identifierCheckBox.setObjectName("identifierCheckBox")
        self.gridLayout.addWidget(self.identifierCheckBox, 0, 0, 1, 1)

        self.retranslateUi(Config)
        QtCore.QMetaObject.connectSlotsByName(Config)

    def retranslateUi(self, Config):
        Config.setWindowTitle(QtGui.QApplication.translate("Config", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("Config", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.configTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Config", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.configTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Config", "Default Value", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("Config", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.identifierCheckBox.setText(QtGui.QApplication.translate("Config", "Define \'Identifier\' configuration value", None, QtGui.QApplication.UnicodeUTF8))

