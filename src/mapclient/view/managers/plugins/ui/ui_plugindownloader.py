# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugindownloader.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_pluginDownloader(object):
    def setupUi(self, pluginDownloader):
        if not pluginDownloader.objectName():
            pluginDownloader.setObjectName(u"pluginDownloader")
        pluginDownloader.resize(737, 563)
        pluginDownloader.setMinimumSize(QSize(450, 250))
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        pluginDownloader.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(pluginDownloader)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(pluginDownloader)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.requiredPlugins = QListWidget(pluginDownloader)
        self.requiredPlugins.setObjectName(u"requiredPlugins")
        self.requiredPlugins.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.requiredPlugins.setProperty("showDropIndicator", False)
        self.requiredPlugins.setDragDropOverwriteMode(False)
        self.requiredPlugins.setWordWrap(True)

        self.verticalLayout.addWidget(self.requiredPlugins)

        self.label_2 = QLabel(pluginDownloader)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.requiredDependencies = QListWidget(pluginDownloader)
        self.requiredDependencies.setObjectName(u"requiredDependencies")

        self.verticalLayout.addWidget(self.requiredDependencies)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pluginDownload = QCheckBox(pluginDownloader)
        self.pluginDownload.setObjectName(u"pluginDownload")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginDownload.sizePolicy().hasHeightForWidth())
        self.pluginDownload.setSizePolicy(sizePolicy)
        self.pluginDownload.setChecked(True)

        self.horizontalLayout_2.addWidget(self.pluginDownload)

        self.dependencyDownload = QCheckBox(pluginDownloader)
        self.dependencyDownload.setObjectName(u"dependencyDownload")
        sizePolicy.setHeightForWidth(self.dependencyDownload.sizePolicy().hasHeightForWidth())
        self.dependencyDownload.setSizePolicy(sizePolicy)
        self.dependencyDownload.setChecked(True)

        self.horizontalLayout_2.addWidget(self.dependencyDownload)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonYes = QPushButton(pluginDownloader)
        self.pushButtonYes.setObjectName(u"pushButtonYes")

        self.horizontalLayout.addWidget(self.pushButtonYes)

        self.pushButtonNo = QPushButton(pluginDownloader)
        self.pushButtonNo.setObjectName(u"pushButtonNo")

        self.horizontalLayout.addWidget(self.pushButtonNo)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(pluginDownloader)
        self.pushButtonYes.clicked.connect(pluginDownloader.accept)
        self.pushButtonNo.clicked.connect(pluginDownloader.reject)

        QMetaObject.connectSlotsByName(pluginDownloader)
    # setupUi

    def retranslateUi(self, pluginDownloader):
        pluginDownloader.setWindowTitle(QCoreApplication.translate("pluginDownloader", u"Workflow Requirements", None))
        self.label.setText(QCoreApplication.translate("pluginDownloader", u"You require the following additional plugins in order to run this workflow:", None))
        self.label_2.setText(QCoreApplication.translate("pluginDownloader", u"This workflow uses the following packages that are not currently installed on your system:", None))
        self.pluginDownload.setText(QCoreApplication.translate("pluginDownloader", u"Download required Plugins", None))
        self.dependencyDownload.setText(QCoreApplication.translate("pluginDownloader", u"Download and install Packages", None))
        self.pushButtonYes.setText(QCoreApplication.translate("pluginDownloader", u"Ok", None))
        self.pushButtonNo.setText(QCoreApplication.translate("pluginDownloader", u"Cancel", None))
    # retranslateUi

