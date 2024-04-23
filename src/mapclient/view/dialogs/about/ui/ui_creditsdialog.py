# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'creditsdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CreditsDialog(object):
    def setupUi(self, CreditsDialog):
        if not CreditsDialog.objectName():
            CreditsDialog.setObjectName(u"CreditsDialog")
        CreditsDialog.resize(475, 356)
        self.verticalLayout = QVBoxLayout(CreditsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_CreditsTab = QFrame(CreditsDialog)
        self.frame_CreditsTab.setObjectName(u"frame_CreditsTab")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_CreditsTab.sizePolicy().hasHeightForWidth())
        self.frame_CreditsTab.setSizePolicy(sizePolicy)
        self.frame_CreditsTab.setFrameShape(QFrame.StyledPanel)
        self.frame_CreditsTab.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.frame_CreditsTab)

        self.frame = QFrame(CreditsDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_Close = QPushButton(self.frame)
        self.btn_Close.setObjectName(u"btn_Close")

        self.horizontalLayout.addWidget(self.btn_Close)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(CreditsDialog)
        self.btn_Close.clicked.connect(CreditsDialog.close)

        QMetaObject.connectSlotsByName(CreditsDialog)
    # setupUi

    def retranslateUi(self, CreditsDialog):
        CreditsDialog.setWindowTitle(QCoreApplication.translate("CreditsDialog", u"MAP Client Credits", None))
        self.btn_Close.setText(QCoreApplication.translate("CreditsDialog", u"&Close", None))
    # retranslateUi

