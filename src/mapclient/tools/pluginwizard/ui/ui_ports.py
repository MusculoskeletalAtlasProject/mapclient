# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ports.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Ports(object):
    def setupUi(self, Ports):
        if not Ports.objectName():
            Ports.setObjectName(u"Ports")
        Ports.resize(400, 300)
        self.gridLayout = QGridLayout(Ports)
        self.gridLayout.setObjectName(u"gridLayout")
        self.addButton = QPushButton(Ports)
        self.addButton.setObjectName(u"addButton")

        self.gridLayout.addWidget(self.addButton, 0, 1, 1, 1)

        self.portTableWidget = QTableWidget(Ports)
        self.portTableWidget.setObjectName(u"portTableWidget")
        self.portTableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.portTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.portTableWidget, 0, 0, 3, 1)

        self.removeButton = QPushButton(Ports)
        self.removeButton.setObjectName(u"removeButton")

        self.gridLayout.addWidget(self.removeButton, 1, 1, 1, 1)


        self.retranslateUi(Ports)

        QMetaObject.connectSlotsByName(Ports)
    # setupUi

    def retranslateUi(self, Ports):
        Ports.setWindowTitle(QCoreApplication.translate("Ports", u"Form", None))
        self.addButton.setText(QCoreApplication.translate("Ports", u"Add", None))
        self.removeButton.setText(QCoreApplication.translate("Ports", u"Remove", None))
    # retranslateUi

