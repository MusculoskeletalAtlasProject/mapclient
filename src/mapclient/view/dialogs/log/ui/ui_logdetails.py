# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/view/dialogs/log/qt/logdetails.ui',
# licensing of 'src/mapclient/view/dialogs/log/qt/logdetails.ui' applies.
#
# Created: Wed Jun 26 16:08:36 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LogDetails(object):
    def setupUi(self, LogDetails):
        LogDetails.setObjectName("LogDetails")
        LogDetails.resize(655, 310)
        LogDetails.setMinimumSize(QtCore.QSize(350, 150))
        LogDetails.setSizeGripEnabled(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(LogDetails)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.detailedTable = QtWidgets.QTableWidget(LogDetails)
        self.detailedTable.setAutoScroll(True)
        self.detailedTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.detailedTable.setTabKeyNavigation(False)
        self.detailedTable.setProperty("showDropIndicator", False)
        self.detailedTable.setDragDropOverwriteMode(False)
        self.detailedTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.detailedTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.detailedTable.setShowGrid(False)
        self.detailedTable.setCornerButtonEnabled(False)
        self.detailedTable.setRowCount(5)
        self.detailedTable.setObjectName("detailedTable")
        self.detailedTable.setColumnCount(0)
        self.detailedTable.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.detailedTable.setVerticalHeaderItem(4, item)
        self.detailedTable.horizontalHeader().setVisible(False)
        self.detailedTable.horizontalHeader().setStretchLastSection(True)
        self.detailedTable.verticalHeader().setDefaultSectionSize(20)
        self.detailedTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.detailedTable)

        self.retranslateUi(LogDetails)
        QtCore.QMetaObject.connectSlotsByName(LogDetails)

    def retranslateUi(self, LogDetails):
        LogDetails.setWindowTitle(QtWidgets.QApplication.translate("LogDetails", "Details", None, -1))
        self.detailedTable.verticalHeaderItem(0).setText(QtWidgets.QApplication.translate("LogDetails", "Date:", None, -1))
        self.detailedTable.verticalHeaderItem(1).setText(QtWidgets.QApplication.translate("LogDetails", "Time:", None, -1))
        self.detailedTable.verticalHeaderItem(2).setText(QtWidgets.QApplication.translate("LogDetails", "Source:", None, -1))
        self.detailedTable.verticalHeaderItem(3).setText(QtWidgets.QApplication.translate("LogDetails", "Level:", None, -1))
        self.detailedTable.verticalHeaderItem(4).setText(QtWidgets.QApplication.translate("LogDetails", "Description:", None, -1))

