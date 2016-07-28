# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pluginprogress.ui'
#
# Created: Thu Dec 11 13:45:34 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DownloadProgress(object):
    def setupUi(self, DownloadProgress):
        DownloadProgress.setObjectName("DownloadProgress")
        DownloadProgress.resize(300, 90)
        DownloadProgress.setMinimumSize(QtCore.QSize(300, 90))
        DownloadProgress.setMaximumSize(QtCore.QSize(300, 108))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DownloadProgress.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(DownloadProgress)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(DownloadProgress)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtGui.QProgressBar(DownloadProgress)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelDownload = QtGui.QPushButton(DownloadProgress)
        self.cancelDownload.setObjectName("cancelDownload")
        self.horizontalLayout.addWidget(self.cancelDownload)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DownloadProgress)
        QtCore.QMetaObject.connectSlotsByName(DownloadProgress)

    def retranslateUi(self, DownloadProgress):
        DownloadProgress.setWindowTitle(QtGui.QApplication.translate("DownloadProgress", "Loading Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelDownload.setText(QtGui.QApplication.translate("DownloadProgress", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
