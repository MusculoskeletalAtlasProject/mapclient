# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/progressdialog.ui'
#
# Created: Tue May 19 22:12:50 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(300, 108)
        ProgressDialog.setMinimumSize(QtCore.QSize(0, 0))
        ProgressDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProgressDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ProgressDialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtGui.QProgressBar(ProgressDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelDownload = QtGui.QPushButton(ProgressDialog)
        self.cancelDownload.setObjectName("cancelDownload")
        self.horizontalLayout.addWidget(self.cancelDownload)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QtGui.QApplication.translate("ProgressDialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelDownload.setText(QtGui.QApplication.translate("ProgressDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
