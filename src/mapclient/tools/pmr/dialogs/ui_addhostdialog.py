# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addhostdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AddHostDialog(object):
    def setupUi(self, AddHostDialog):
        if not AddHostDialog.objectName():
            AddHostDialog.setObjectName(u"AddHostDialog")
        AddHostDialog.resize(360, 104)
        self.verticalLayout = QVBoxLayout(AddHostDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(AddHostDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.urlLineEdit = QLineEdit(self.groupBox)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.horizontalLayout.addWidget(self.urlLineEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(AddHostDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddHostDialog)
        self.buttonBox.accepted.connect(AddHostDialog.accept)
        self.buttonBox.rejected.connect(AddHostDialog.reject)

        QMetaObject.connectSlotsByName(AddHostDialog)
    # setupUi

    def retranslateUi(self, AddHostDialog):
        AddHostDialog.setWindowTitle(QCoreApplication.translate("AddHostDialog", u"Add Host", None))
        self.groupBox.setTitle(QCoreApplication.translate("AddHostDialog", u"PMR Web Address", None))
        self.label.setText(QCoreApplication.translate("AddHostDialog", u"url: ", None))
    # retranslateUi

