# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.resize(300, 108)
        ProgressDialog.setMinimumSize(QSize(0, 0))
        ProgressDialog.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        ProgressDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ProgressDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(ProgressDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancelDownload = QPushButton(ProgressDialog)
        self.cancelDownload.setObjectName(u"cancelDownload")

        self.horizontalLayout.addWidget(self.cancelDownload)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ProgressDialog)

        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Progress", None))
        self.label.setText("")
        self.cancelDownload.setText(QCoreApplication.translate("ProgressDialog", u"Cancel", None))
    # retranslateUi

