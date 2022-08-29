# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'provenancedialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ProvenanceDialog(object):
    def setupUi(self, ProvenanceDialog):
        if not ProvenanceDialog.objectName():
            ProvenanceDialog.setObjectName(u"ProvenanceDialog")
        ProvenanceDialog.resize(475, 356)
        self.verticalLayout = QVBoxLayout(ProvenanceDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(ProvenanceDialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget = QTableWidget(self.frame_2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.tableWidget)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(ProvenanceDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_Close = QPushButton(self.frame)
        self.btn_Close.setObjectName(u"btn_Close")

        self.horizontalLayout.addWidget(self.btn_Close)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(ProvenanceDialog)
        self.btn_Close.clicked.connect(ProvenanceDialog.close)

        QMetaObject.connectSlotsByName(ProvenanceDialog)
    # setupUi

    def retranslateUi(self, ProvenanceDialog):
        ProvenanceDialog.setWindowTitle(QCoreApplication.translate("ProvenanceDialog", u"MAP Client Provenance", None))
        self.btn_Close.setText(QCoreApplication.translate("ProvenanceDialog", u"&Close", None))
    # retranslateUi

