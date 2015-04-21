# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/ports.ui'
#
# Created: Fri Oct 11 15:59:32 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Ports(object):
    def setupUi(self, Ports):
        Ports.setObjectName("Ports")
        Ports.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Ports)
        self.gridLayout.setObjectName("gridLayout")
        self.addButton = QtGui.QPushButton(Ports)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 0, 1, 1, 1)
        self.portTableWidget = QtGui.QTableWidget(Ports)
        self.portTableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.portTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.portTableWidget.setObjectName("portTableWidget")
        self.portTableWidget.setColumnCount(0)
        self.portTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.portTableWidget, 0, 0, 3, 1)
        self.removeButton = QtGui.QPushButton(Ports)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)

        self.retranslateUi(Ports)
        QtCore.QMetaObject.connectSlotsByName(Ports)

    def retranslateUi(self, Ports):
        Ports.setWindowTitle(QtGui.QApplication.translate("Ports", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("Ports", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("Ports", "Remove", None, QtGui.QApplication.UnicodeUTF8))

