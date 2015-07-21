# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/loadlogsession.ui'
#
# Created: Tue Dec  2 10:43:58 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoadWindow(object):
    def setupUi(self, LoadWindow):
        LoadWindow.setObjectName("LoadWindow")
        LoadWindow.resize(550, 75)
        LoadWindow.setMinimumSize(QtCore.QSize(550, 75))
        LoadWindow.setMaximumSize(QtCore.QSize(550, 75))
        LoadWindow.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(LoadWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.file = QtGui.QLabel(LoadWindow)
        self.file.setObjectName("file")
        self.horizontalLayout_2.addWidget(self.file)
        self.lineEdit = QtGui.QLineEdit(LoadWindow)
        self.lineEdit.setAcceptDrops(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.searchButton = QtGui.QPushButton(LoadWindow)
        self.searchButton.setMinimumSize(QtCore.QSize(40, 23))
        self.searchButton.setMaximumSize(QtCore.QSize(40, 23))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loadButton = QtGui.QPushButton(LoadWindow)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout.addWidget(self.loadButton)
        self.cancelButton = QtGui.QPushButton(LoadWindow)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoadWindow)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), LoadWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadWindow)

    def retranslateUi(self, LoadWindow):
        LoadWindow.setWindowTitle(QtGui.QApplication.translate("LoadWindow", "Load Previous Session", None, QtGui.QApplication.UnicodeUTF8))
        self.file.setText(QtGui.QApplication.translate("LoadWindow", "File:", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("LoadWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("LoadWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("LoadWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

