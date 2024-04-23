# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checkstatusdialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_CheckStatusDialog(object):
    def setupUi(self, CheckStatusDialog):
        if not CheckStatusDialog.objectName():
            CheckStatusDialog.setObjectName(u"CheckStatusDialog")
        CheckStatusDialog.resize(548, 284)
        self.verticalLayout = QVBoxLayout(CheckStatusDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(CheckStatusDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.labelCheckTitle = QLabel(CheckStatusDialog)
        self.labelCheckTitle.setObjectName(u"labelCheckTitle")

        self.horizontalLayout.addWidget(self.labelCheckTitle)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEditScreen = QPlainTextEdit(CheckStatusDialog)
        self.plainTextEditScreen.setObjectName(u"plainTextEditScreen")

        self.verticalLayout.addWidget(self.plainTextEditScreen)

        self.label_2 = QLabel(CheckStatusDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.label_2)

        self.buttonBox = QDialogButtonBox(CheckStatusDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CheckStatusDialog)
        self.buttonBox.accepted.connect(CheckStatusDialog.accept)
        self.buttonBox.rejected.connect(CheckStatusDialog.reject)

        QMetaObject.connectSlotsByName(CheckStatusDialog)
    # setupUi

    def retranslateUi(self, CheckStatusDialog):
        CheckStatusDialog.setWindowTitle(QCoreApplication.translate("CheckStatusDialog", u"Checking Application Status", None))
        self.label.setText(QCoreApplication.translate("CheckStatusDialog", u"Checking Status:", None))
        self.labelCheckTitle.setText(QCoreApplication.translate("CheckStatusDialog", u"placeholder", None))
        self.label_2.setText(QCoreApplication.translate("CheckStatusDialog", u"Use the 'Options' dialog accessible from the 'View' menu to resolve problems shown here.  Some MAP Client features will not be available if errors have been reported.", None))
    # retranslateUi

