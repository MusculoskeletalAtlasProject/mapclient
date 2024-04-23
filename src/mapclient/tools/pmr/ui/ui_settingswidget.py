# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingswidget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        if not SettingsWidget.objectName():
            SettingsWidget.setObjectName(u"SettingsWidget")
        SettingsWidget.resize(498, 476)
        self.actionAddHost = QAction(SettingsWidget)
        self.actionAddHost.setObjectName(u"actionAddHost")
        self.verticalLayout_2 = QVBoxLayout(SettingsWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(SettingsWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.hostListView = QListView(SettingsWidget)
        self.hostListView.setObjectName(u"hostListView")
        self.hostListView.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.horizontalLayout.addWidget(self.hostListView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addPushButton = QPushButton(SettingsWidget)
        self.addPushButton.setObjectName(u"addPushButton")

        self.verticalLayout.addWidget(self.addPushButton)

        self.removePushButton = QPushButton(SettingsWidget)
        self.removePushButton.setObjectName(u"removePushButton")

        self.verticalLayout.addWidget(self.removePushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(SettingsWidget)

        QMetaObject.connectSlotsByName(SettingsWidget)
    # setupUi

    def retranslateUi(self, SettingsWidget):
        SettingsWidget.setWindowTitle(QCoreApplication.translate("SettingsWidget", u"Settings", None))
        self.actionAddHost.setText(QCoreApplication.translate("SettingsWidget", u"Add Host", None))
        self.label.setText(QCoreApplication.translate("SettingsWidget", u"Host list:", None))
        self.addPushButton.setText(QCoreApplication.translate("SettingsWidget", u"Add", None))
        self.removePushButton.setText(QCoreApplication.translate("SettingsWidget", u"Remove", None))
    # retranslateUi

