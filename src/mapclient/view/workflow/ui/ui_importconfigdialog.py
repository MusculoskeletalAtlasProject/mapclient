# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importconfigdialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ImportConfigDialog(object):
    def setupUi(self, ImportConfigDialog):
        if not ImportConfigDialog.objectName():
            ImportConfigDialog.setObjectName(u"ImportConfigDialog")
        ImportConfigDialog.resize(700, 500)
        self.verticalLayout = QVBoxLayout(ImportConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(ImportConfigDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_1 = QLabel(self.groupBox)
        self.label_1.setObjectName(u"label_1")

        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonImport = QPushButton(ImportConfigDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout_2.addWidget(self.pushButtonImport)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(ImportConfigDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout_2.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.pushButtonImport, self.pushButtonClose)

        self.retranslateUi(ImportConfigDialog)
        self.pushButtonClose.clicked.connect(ImportConfigDialog.reject)

        QMetaObject.connectSlotsByName(ImportConfigDialog)
    # setupUi

    def retranslateUi(self, ImportConfigDialog):
        ImportConfigDialog.setWindowTitle(QCoreApplication.translate("ImportConfigDialog", u"Import Workflow Configuration", None))
        self.groupBox.setTitle("")
        self.label_2.setText(QCoreApplication.translate("ImportConfigDialog", u"Step Type:", None))
        self.label_1.setText(QCoreApplication.translate("ImportConfigDialog", u"Workflow Step ID:", None))
        self.label_3.setText(QCoreApplication.translate("ImportConfigDialog", u"Import Configuration From:", None))
        self.pushButtonImport.setText(QCoreApplication.translate("ImportConfigDialog", u"Import", None))
        self.pushButtonClose.setText(QCoreApplication.translate("ImportConfigDialog", u"Close", None))
    # retranslateUi

