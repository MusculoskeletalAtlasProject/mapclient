# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/searchwidget.ui'
#
# Created: Tue Mar  3 09:01:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        SearchWidget.setObjectName("SearchWidget")
        SearchWidget.resize(466, 480)
        self.verticalLayout = QtGui.QVBoxLayout(SearchWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchLineEdit = QtGui.QLineEdit(SearchWidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout_3.addWidget(self.searchLineEdit)
        self.searchButton = QtGui.QPushButton(SearchWidget)
        self.searchButton.setDefault(True)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_3.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_2 = QtGui.QLabel(SearchWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.searchResultsListWidget = QtGui.QListWidget(SearchWidget)
        self.searchResultsListWidget.setObjectName("searchResultsListWidget")
        self.verticalLayout.addWidget(self.searchResultsListWidget)
        self.label_3 = QtGui.QLabel(SearchWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.targetEdit = QtGui.QLineEdit(SearchWidget)
        self.targetEdit.setObjectName("targetEdit")
        self.verticalLayout.addWidget(self.targetEdit)

        self.retranslateUi(SearchWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchWidget)

    def retranslateUi(self, SearchWidget):
        SearchWidget.setWindowTitle(QtGui.QApplication.translate("SearchWidget", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("SearchWidget", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SearchWidget", "Search results:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SearchWidget", "Result target:", None, QtGui.QApplication.UnicodeUTF8))

