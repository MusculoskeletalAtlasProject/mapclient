# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'authoriseapplicationdialog.ui'
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
    QGroupBox, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_AuthoriseApplicationDialog(object):
    def setupUi(self, AuthoriseApplicationDialog):
        if not AuthoriseApplicationDialog.objectName():
            AuthoriseApplicationDialog.setObjectName(u"AuthoriseApplicationDialog")
        AuthoriseApplicationDialog.resize(482, 300)
        self.verticalLayout = QVBoxLayout(AuthoriseApplicationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(AuthoriseApplicationDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.tokenLineEdit = QLineEdit(self.groupBox)
        self.tokenLineEdit.setObjectName(u"tokenLineEdit")

        self.verticalLayout_2.addWidget(self.tokenLineEdit)

        self.verticalSpacer = QSpacerItem(20, 122, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(AuthoriseApplicationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AuthoriseApplicationDialog)
        self.buttonBox.rejected.connect(AuthoriseApplicationDialog.reject)
        self.buttonBox.accepted.connect(AuthoriseApplicationDialog.accept)

        QMetaObject.connectSlotsByName(AuthoriseApplicationDialog)
    # setupUi

    def retranslateUi(self, AuthoriseApplicationDialog):
        AuthoriseApplicationDialog.setWindowTitle(QCoreApplication.translate("AuthoriseApplicationDialog", u"Authorise Application", None))
        self.groupBox.setTitle(QCoreApplication.translate("AuthoriseApplicationDialog", u"Authorise Application", None))
        self.label.setText(QCoreApplication.translate("AuthoriseApplicationDialog", u"Paste authorisation token here:", None))
    # retranslateUi

