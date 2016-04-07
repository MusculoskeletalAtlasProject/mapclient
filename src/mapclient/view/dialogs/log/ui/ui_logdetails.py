# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\logdetails.ui'
#
# Created: Wed Apr  6 22:54:09 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LogDetails(object):
    def setupUi(self, LogDetails):
        LogDetails.setObjectName("LogDetails")
        LogDetails.resize(655, 310)
        LogDetails.setMinimumSize(QtCore.QSize(350, 150))
        LogDetails.setSizeGripEnabled(False)
        self.horizontalLayout = QtGui.QHBoxLayout(LogDetails)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.detailedTable = QtGui.QTableWidget(LogDetails)
        self.detailedTable.setAutoScroll(True)
        self.detailedTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.detailedTable.setTabKeyNavigation(False)
        self.detailedTable.setProperty("showDropIndicator", False)
        self.detailedTable.setDragDropOverwriteMode(False)
        self.detailedTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.detailedTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.detailedTable.setShowGrid(False)
        self.detailedTable.setCornerButtonEnabled(False)
        self.detailedTable.setRowCount(5)
        self.detailedTable.setObjectName("detailedTable")
        self.detailedTable.setColumnCount(0)
        self.detailedTable.setRowCount(5)
        item = QtGui.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(4, item)
        self.detailedTable.horizontalHeader().setVisible(False)
        self.detailedTable.horizontalHeader().setStretchLastSection(True)
        self.detailedTable.verticalHeader().setDefaultSectionSize(20)
        self.detailedTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.detailedTable)

        self.retranslateUi(LogDetails)
        QtCore.QMetaObject.connectSlotsByName(LogDetails)

    def retranslateUi(self, LogDetails):
        LogDetails.setWindowTitle(QtGui.QApplication.translate("LogDetails", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.detailedTable.verticalHeaderItem(0).setText(QtGui.QApplication.translate("LogDetails", "Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.detailedTable.verticalHeaderItem(1).setText(QtGui.QApplication.translate("LogDetails", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.detailedTable.verticalHeaderItem(2).setText(QtGui.QApplication.translate("LogDetails", "Source:", None, QtGui.QApplication.UnicodeUTF8))
        self.detailedTable.verticalHeaderItem(3).setText(QtGui.QApplication.translate("LogDetails", "Level:", None, QtGui.QApplication.UnicodeUTF8))
        self.detailedTable.verticalHeaderItem(4).setText(QtGui.QApplication.translate("LogDetails", "Description:", None, QtGui.QApplication.UnicodeUTF8))

