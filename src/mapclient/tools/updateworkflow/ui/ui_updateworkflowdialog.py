# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updateworkflowdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UpdateWorkflowDialog(object):
    def setupUi(self, UpdateWorkflowDialog):
        if not UpdateWorkflowDialog.objectName():
            UpdateWorkflowDialog.setObjectName(u"UpdateWorkflowDialog")
        UpdateWorkflowDialog.resize(491, 153)
        self.verticalLayout = QVBoxLayout(UpdateWorkflowDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(UpdateWorkflowDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditStepLocation = QLineEdit(self.groupBox)
        self.lineEditStepLocation.setObjectName(u"lineEditStepLocation")

        self.horizontalLayout.addWidget(self.lineEditStepLocation)

        self.pushButtonStepChooser = QPushButton(self.groupBox)
        self.pushButtonStepChooser.setObjectName(u"pushButtonStepChooser")

        self.horizontalLayout.addWidget(self.pushButtonStepChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonUpdate = QPushButton(UpdateWorkflowDialog)
        self.pushButtonUpdate.setObjectName(u"pushButtonUpdate")

        self.horizontalLayout_2.addWidget(self.pushButtonUpdate)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(UpdateWorkflowDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout_2.addWidget(self.pushButtonClose)

        self.pushButtonCancel = QPushButton(UpdateWorkflowDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_2.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.lineEditStepLocation, self.pushButtonStepChooser)
        QWidget.setTabOrder(self.pushButtonStepChooser, self.pushButtonUpdate)
        QWidget.setTabOrder(self.pushButtonUpdate, self.pushButtonCancel)

        self.retranslateUi(UpdateWorkflowDialog)
        self.pushButtonCancel.clicked.connect(UpdateWorkflowDialog.reject)
        self.pushButtonClose.clicked.connect(UpdateWorkflowDialog.reject)

        QMetaObject.connectSlotsByName(UpdateWorkflowDialog)
    # setupUi

    def retranslateUi(self, UpdateWorkflowDialog):
        UpdateWorkflowDialog.setWindowTitle(QCoreApplication.translate("UpdateWorkflowDialog", u"Update Workflow Tool", None))
        self.groupBox.setTitle("")
        self.label_4.setText(QCoreApplication.translate("UpdateWorkflowDialog", u"Workflow to update (location on disk):", None))
#if QT_CONFIG(tooltip)
        self.pushButtonStepChooser.setToolTip(QCoreApplication.translate("UpdateWorkflowDialog", u"Choose workflow directory to update", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonStepChooser.setText(QCoreApplication.translate("UpdateWorkflowDialog", u"...", None))
        self.pushButtonUpdate.setText(QCoreApplication.translate("UpdateWorkflowDialog", u"Update", None))
        self.pushButtonClose.setText(QCoreApplication.translate("UpdateWorkflowDialog", u"Close", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("UpdateWorkflowDialog", u"Cancel", None))
    # retranslateUi

