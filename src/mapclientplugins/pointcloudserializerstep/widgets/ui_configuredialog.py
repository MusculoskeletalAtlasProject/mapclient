# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(526, 216)
        self.verticalLayout_2 = QVBoxLayout(ConfigureDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(ConfigureDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEditOutputLocation = QLineEdit(self.groupBox)
        self.lineEditOutputLocation.setObjectName(u"lineEditOutputLocation")

        self.horizontalLayout_2.addWidget(self.lineEditOutputLocation)

        self.pushButtonOutputLocation = QPushButton(self.groupBox)
        self.pushButtonOutputLocation.setObjectName(u"pushButtonOutputLocation")

        self.horizontalLayout_2.addWidget(self.pushButtonOutputLocation)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.checkBoxDefaultLocation = QCheckBox(self.groupBox)
        self.checkBoxDefaultLocation.setObjectName(u"checkBoxDefaultLocation")
        self.checkBoxDefaultLocation.setChecked(True)

        self.verticalLayout.addWidget(self.checkBoxDefaultLocation)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure - Point Cloud Store", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("ConfigureDialog", u"Output:", None))
        self.pushButtonOutputLocation.setText(QCoreApplication.translate("ConfigureDialog", u"...", None))
        self.checkBoxDefaultLocation.setText(QCoreApplication.translate("ConfigureDialog", u"Use output default location", None))
    # retranslateUi

