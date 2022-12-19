# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'oauthcheckdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_OAuthCheckDialog(object):
    def setupUi(self, OAuthCheckDialog):
        if not OAuthCheckDialog.objectName():
            OAuthCheckDialog.setObjectName(u"OAuthCheckDialog")
        OAuthCheckDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(OAuthCheckDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(OAuthCheckDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.continueButton = QPushButton(self.groupBox)
        self.continueButton.setObjectName(u"continueButton")

        self.verticalLayout_2.addWidget(self.continueButton)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(OAuthCheckDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(OAuthCheckDialog)
        self.buttonBox.accepted.connect(OAuthCheckDialog.accept)
        self.buttonBox.rejected.connect(OAuthCheckDialog.reject)

        self.continueButton.setDefault(True)


        QMetaObject.connectSlotsByName(OAuthCheckDialog)
    # setupUi

    def retranslateUi(self, OAuthCheckDialog):
        OAuthCheckDialog.setWindowTitle(QCoreApplication.translate("OAuthCheckDialog", u"Access Credentials Required", None))
        self.groupBox.setTitle(QCoreApplication.translate("OAuthCheckDialog", u"Authorise Application", None))
        self.label.setText(QCoreApplication.translate("OAuthCheckDialog", u"MAP Client requires your permission to access PMR.", None))
        self.continueButton.setText(QCoreApplication.translate("OAuthCheckDialog", u"Continue", None))
    # retranslateUi

