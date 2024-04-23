# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadlogsession.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LoadWindow(object):
    def setupUi(self, LoadWindow):
        if not LoadWindow.objectName():
            LoadWindow.setObjectName(u"LoadWindow")
        LoadWindow.resize(558, 134)
        LoadWindow.setModal(True)
        self.verticalLayout = QVBoxLayout(LoadWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 11)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.file = QLabel(LoadWindow)
        self.file.setObjectName(u"file")

        self.horizontalLayout_2.addWidget(self.file)

        self.lineEdit = QLineEdit(LoadWindow)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAcceptDrops(False)
        self.lineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(LoadWindow)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setMinimumSize(QSize(40, 23))
        self.searchButton.setMaximumSize(QSize(40, 23))

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(58, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.loadButton = QPushButton(LoadWindow)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout.addWidget(self.loadButton)

        self.cancelButton = QPushButton(LoadWindow)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LoadWindow)
        self.cancelButton.clicked.connect(LoadWindow.reject)

        QMetaObject.connectSlotsByName(LoadWindow)
    # setupUi

    def retranslateUi(self, LoadWindow):
        LoadWindow.setWindowTitle(QCoreApplication.translate("LoadWindow", u"Load Previous Session", None))
        self.file.setText(QCoreApplication.translate("LoadWindow", u"File:", None))
        self.searchButton.setText(QCoreApplication.translate("LoadWindow", u"...", None))
        self.loadButton.setText(QCoreApplication.translate("LoadWindow", u"Load", None))
        self.cancelButton.setText(QCoreApplication.translate("LoadWindow", u"Cancel", None))
    # retranslateUi

