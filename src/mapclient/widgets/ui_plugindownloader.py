# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/plugindownloader.ui'
#
# Created: Tue Dec 16 12:11:47 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_pluginDownloader(object):
    def setupUi(self, pluginDownloader):
        pluginDownloader.setObjectName("pluginDownloader")
        pluginDownloader.resize(600, 250)
        pluginDownloader.setMinimumSize(QtCore.QSize(600, 250))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pluginDownloader.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(pluginDownloader)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(pluginDownloader)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.requiredPlugins = QtGui.QListWidget(pluginDownloader)
        self.requiredPlugins.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.requiredPlugins.setProperty("showDropIndicator", False)
        self.requiredPlugins.setDragDropOverwriteMode(False)
        self.requiredPlugins.setObjectName("requiredPlugins")
        self.verticalLayout.addWidget(self.requiredPlugins)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.downloadPrompt = QtGui.QLabel(pluginDownloader)
        self.downloadPrompt.setObjectName("downloadPrompt")
        self.horizontalLayout.addWidget(self.downloadPrompt)
        spacerItem = QtGui.QSpacerItem(148, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonYes = QtGui.QPushButton(pluginDownloader)
        self.pushButtonYes.setObjectName("pushButtonYes")
        self.horizontalLayout.addWidget(self.pushButtonYes)
        self.pushButtonNo = QtGui.QPushButton(pluginDownloader)
        self.pushButtonNo.setObjectName("pushButtonNo")
        self.horizontalLayout.addWidget(self.pushButtonNo)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(pluginDownloader)
        QtCore.QObject.connect(self.pushButtonYes, QtCore.SIGNAL("clicked()"), pluginDownloader.accept)
        QtCore.QObject.connect(self.pushButtonNo, QtCore.SIGNAL("clicked()"), pluginDownloader.reject)
        QtCore.QMetaObject.connectSlotsByName(pluginDownloader)

    def retranslateUi(self, pluginDownloader):
        pluginDownloader.setWindowTitle(QtGui.QApplication.translate("pluginDownloader", "Plugin Downloader", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("pluginDownloader", "You require the following additional plugins in order to run this workflow:", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadPrompt.setText(QtGui.QApplication.translate("pluginDownloader", "Would you like to download them?", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonYes.setText(QtGui.QApplication.translate("pluginDownloader", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNo.setText(QtGui.QApplication.translate("pluginDownloader", "No", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
