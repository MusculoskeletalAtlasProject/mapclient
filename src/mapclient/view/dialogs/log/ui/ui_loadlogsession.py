# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/view/dialogs/log/qt/loadlogsession.ui',
# licensing of 'src/mapclient/view/dialogs/log/qt/loadlogsession.ui' applies.
#
# Created: Wed Jun 26 16:08:29 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoadWindow(object):
    def setupUi(self, LoadWindow):
        LoadWindow.setObjectName("LoadWindow")
        LoadWindow.resize(558, 134)
        LoadWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.file = QtWidgets.QLabel(LoadWindow)
        self.file.setObjectName("file")
        self.horizontalLayout_2.addWidget(self.file)
        self.lineEdit = QtWidgets.QLineEdit(LoadWindow)
        self.lineEdit.setAcceptDrops(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.searchButton = QtWidgets.QPushButton(LoadWindow)
        self.searchButton.setMinimumSize(QtCore.QSize(40, 23))
        self.searchButton.setMaximumSize(QtCore.QSize(40, 23))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(58, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loadButton = QtWidgets.QPushButton(LoadWindow)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout.addWidget(self.loadButton)
        self.cancelButton = QtWidgets.QPushButton(LoadWindow)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoadWindow)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), LoadWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadWindow)

    def retranslateUi(self, LoadWindow):
        LoadWindow.setWindowTitle(QtWidgets.QApplication.translate("LoadWindow", "Load Previous Session", None, -1))
        self.file.setText(QtWidgets.QApplication.translate("LoadWindow", "File:", None, -1))
        self.searchButton.setText(QtWidgets.QApplication.translate("LoadWindow", "...", None, -1))
        self.loadButton.setText(QtWidgets.QApplication.translate("LoadWindow", "Load", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("LoadWindow", "Cancel", None, -1))

