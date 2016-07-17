# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/plugindownloader.ui'
#
# Created: Wed Apr  8 14:14:36 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_pluginDownloader(object):
    def setupUi(self, pluginDownloader):
        pluginDownloader.setObjectName("pluginDownloader")
        pluginDownloader.resize(511, 411)
        pluginDownloader.setMinimumSize(QtCore.QSize(450, 250))
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
        self.requiredPlugins.setWordWrap(True)
        self.requiredPlugins.setObjectName("requiredPlugins")
        self.verticalLayout.addWidget(self.requiredPlugins)
        self.label_2 = QtGui.QLabel(pluginDownloader)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.requiredDependencies = QtGui.QListWidget(pluginDownloader)
        self.requiredDependencies.setObjectName("requiredDependencies")
        self.verticalLayout.addWidget(self.requiredDependencies)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pluginDownload = QtGui.QCheckBox(pluginDownloader)
        self.pluginDownload.setChecked(True)
        self.pluginDownload.setObjectName("pluginDownload")
        self.horizontalLayout_2.addWidget(self.pluginDownload)
        self.dependencyDownload = QtGui.QCheckBox(pluginDownloader)
        self.dependencyDownload.setChecked(True)
        self.dependencyDownload.setObjectName("dependencyDownload")
        self.horizontalLayout_2.addWidget(self.dependencyDownload)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        pluginDownloader.setWindowTitle(QtGui.QApplication.translate("pluginDownloader", "Workflow Requirements", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("pluginDownloader", "You require the following additional plugins in order to run this workflow:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("pluginDownloader", "This workflow uses the following packages that are not currently installed on your system:", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginDownload.setText(QtGui.QApplication.translate("pluginDownloader", "Download required Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.dependencyDownload.setText(QtGui.QApplication.translate("pluginDownloader", "Download and install Packages", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonYes.setText(QtGui.QApplication.translate("pluginDownloader", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNo.setText(QtGui.QApplication.translate("pluginDownloader", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
