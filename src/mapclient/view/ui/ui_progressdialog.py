# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressdialog.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.resize(300, 108)
        ProgressDialog.setMinimumSize(QSize(0, 0))
        ProgressDialog.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        ProgressDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ProgressDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(ProgressDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancelDownload = QPushButton(ProgressDialog)
        self.cancelDownload.setObjectName(u"cancelDownload")

        self.horizontalLayout.addWidget(self.cancelDownload)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ProgressDialog)

        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Progress", None))
        self.label.setText("")
        self.cancelDownload.setText(QCoreApplication.translate("ProgressDialog", u"Cancel", None))
    # retranslateUi

