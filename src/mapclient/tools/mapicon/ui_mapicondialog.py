# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mapicondialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MAPIconDialog(object):
    def setupUi(self, MAPIconDialog):
        if not MAPIconDialog.objectName():
            MAPIconDialog.setObjectName(u"MAPIconDialog")
        MAPIconDialog.resize(546, 311)
        self.gridLayout = QGridLayout(MAPIconDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelStepIcon = QLabel(MAPIconDialog)
        self.labelStepIcon.setObjectName(u"labelStepIcon")

        self.gridLayout.addWidget(self.labelStepIcon, 0, 0, 1, 1)

        self.lineEditStepIcon = QLineEdit(MAPIconDialog)
        self.lineEditStepIcon.setObjectName(u"lineEditStepIcon")
        self.lineEditStepIcon.setEnabled(True)

        self.gridLayout.addWidget(self.lineEditStepIcon, 0, 1, 1, 1)

        self.pushButtonStepIcon = QPushButton(MAPIconDialog)
        self.pushButtonStepIcon.setObjectName(u"pushButtonStepIcon")

        self.gridLayout.addWidget(self.pushButtonStepIcon, 0, 2, 1, 1)

        self.labelBackgroundIcon = QLabel(MAPIconDialog)
        self.labelBackgroundIcon.setObjectName(u"labelBackgroundIcon")

        self.gridLayout.addWidget(self.labelBackgroundIcon, 1, 0, 1, 1)

        self.lineEditBackgroundIcon = QLineEdit(MAPIconDialog)
        self.lineEditBackgroundIcon.setObjectName(u"lineEditBackgroundIcon")

        self.gridLayout.addWidget(self.lineEditBackgroundIcon, 1, 1, 1, 1)

        self.pushButtonBackgroundIcon = QPushButton(MAPIconDialog)
        self.pushButtonBackgroundIcon.setObjectName(u"pushButtonBackgroundIcon")

        self.gridLayout.addWidget(self.pushButtonBackgroundIcon, 1, 2, 1, 1)

        self.labelCombinedIcon = QLabel(MAPIconDialog)
        self.labelCombinedIcon.setObjectName(u"labelCombinedIcon")

        self.gridLayout.addWidget(self.labelCombinedIcon, 2, 0, 1, 1)

        self.lineEditCombinedIcon = QLineEdit(MAPIconDialog)
        self.lineEditCombinedIcon.setObjectName(u"lineEditCombinedIcon")

        self.gridLayout.addWidget(self.lineEditCombinedIcon, 2, 1, 1, 1)

        self.pushButtonCombinedIcon = QPushButton(MAPIconDialog)
        self.pushButtonCombinedIcon.setObjectName(u"pushButtonCombinedIcon")

        self.gridLayout.addWidget(self.pushButtonCombinedIcon, 2, 2, 1, 1)

        self.frame = QFrame(MAPIconDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 72))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.frame.setFont(font)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(u"QFrame {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 aliceblue, stop:1 lightskyblue);}\n"
"QLabel {background-color: transparent}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelIconPicture = QLabel(self.frame)
        self.labelIconPicture.setObjectName(u"labelIconPicture")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelIconPicture.sizePolicy().hasHeightForWidth())
        self.labelIconPicture.setSizePolicy(sizePolicy)
        self.labelIconPicture.setMinimumSize(QSize(64, 64))
        self.labelIconPicture.setMaximumSize(QSize(64, 64))
        self.labelIconPicture.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelIconPicture, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(MAPIconDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)

#if QT_CONFIG(shortcut)
        self.labelStepIcon.setBuddy(self.lineEditCombinedIcon)
        self.labelCombinedIcon.setBuddy(self.lineEditStepIcon)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MAPIconDialog)
        self.buttonBox.accepted.connect(MAPIconDialog.accept)
        self.buttonBox.rejected.connect(MAPIconDialog.reject)

        QMetaObject.connectSlotsByName(MAPIconDialog)
    # setupUi

    def retranslateUi(self, MAPIconDialog):
        MAPIconDialog.setWindowTitle(QCoreApplication.translate("MAPIconDialog", u"MAP Icon Dialog", None))
        self.labelStepIcon.setText(QCoreApplication.translate("MAPIconDialog", u"S&tep Icon:", None))
#if QT_CONFIG(tooltip)
        self.lineEditStepIcon.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButtonStepIcon.setText(QCoreApplication.translate("MAPIconDialog", u"...", None))
        self.labelBackgroundIcon.setText(QCoreApplication.translate("MAPIconDialog", u"Background Icon:", None))
        self.pushButtonBackgroundIcon.setText(QCoreApplication.translate("MAPIconDialog", u"...", None))
        self.labelCombinedIcon.setText(QCoreApplication.translate("MAPIconDialog", u"Combi&ned Icon:", None))
        self.pushButtonCombinedIcon.setText(QCoreApplication.translate("MAPIconDialog", u"...", None))
        self.labelIconPicture.setText(QCoreApplication.translate("MAPIconDialog", u"Icon", None))
    # retranslateUi

