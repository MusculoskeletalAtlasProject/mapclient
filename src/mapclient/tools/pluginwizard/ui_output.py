# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'output.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_Output(object):
    def setupUi(self, Output):
        if not Output.objectName():
            Output.setObjectName(u"Output")
        Output.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Output)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.directoryLabel = QLabel(Output)
        self.directoryLabel.setObjectName(u"directoryLabel")

        self.horizontalLayout.addWidget(self.directoryLabel)

        self.directoryLineEdit = QLineEdit(Output)
        self.directoryLineEdit.setObjectName(u"directoryLineEdit")

        self.horizontalLayout.addWidget(self.directoryLineEdit)

        self.directoryButton = QPushButton(Output)
        self.directoryButton.setObjectName(u"directoryButton")

        self.horizontalLayout.addWidget(self.directoryButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 252, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Output)

        QMetaObject.connectSlotsByName(Output)
    # setupUi

    def retranslateUi(self, Output):
        Output.setWindowTitle(QCoreApplication.translate("Output", u"Form", None))
        self.directoryLabel.setText(QCoreApplication.translate("Output", u"Output directory:  ", None))
#if QT_CONFIG(tooltip)
        self.directoryLineEdit.setToolTip(QCoreApplication.translate("Output", u"directory must exist and be writable", None))
#endif // QT_CONFIG(tooltip)
        self.directoryButton.setText(QCoreApplication.translate("Output", u"...", None))
    # retranslateUi

