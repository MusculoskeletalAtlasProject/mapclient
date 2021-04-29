# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registerdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mapclient.tools.pmr.widgets.settingswidget import SettingsWidget


class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        if not RegisterDialog.objectName():
            RegisterDialog.setObjectName(u"RegisterDialog")
        RegisterDialog.resize(433, 489)
        self.verticalLayout = QVBoxLayout(RegisterDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(RegisterDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(RegisterDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.registerTab = QWidget()
        self.registerTab.setObjectName(u"registerTab")
        self.verticalLayout_2 = QVBoxLayout(self.registerTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidgetRegister = QStackedWidget(self.registerTab)
        self.stackedWidgetRegister.setObjectName(u"stackedWidgetRegister")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonRegister = QPushButton(self.page)
        self.pushButtonRegister.setObjectName(u"pushButtonRegister")

        self.horizontalLayout_2.addWidget(self.pushButtonRegister)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 142, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.stackedWidgetRegister.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonDeregister = QPushButton(self.page_2)
        self.pushButtonDeregister.setObjectName(u"pushButtonDeregister")

        self.horizontalLayout_3.addWidget(self.pushButtonDeregister)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_3 = QSpacerItem(20, 142, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.stackedWidgetRegister.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.stackedWidgetRegister)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.registerTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.horizontalLayout_5 = QHBoxLayout(self.settingsTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.settingsWidget = SettingsWidget(self.settingsTab)
        self.settingsWidget.setObjectName(u"settingsWidget")

        self.horizontalLayout_5.addWidget(self.settingsWidget)

        self.tabWidget.addTab(self.settingsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(RegisterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(RegisterDialog)
        self.buttonBox.accepted.connect(RegisterDialog.accept)
        self.buttonBox.rejected.connect(RegisterDialog.reject)

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidgetRegister.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RegisterDialog)
    # setupUi

    def retranslateUi(self, RegisterDialog):
        RegisterDialog.setWindowTitle(QCoreApplication.translate("RegisterDialog", u"PMR Register", None))
        self.label.setText(QCoreApplication.translate("RegisterDialog", u"Physiome Model Repository", None))
        self.pushButtonRegister.setText(QCoreApplication.translate("RegisterDialog", u"&Register", None))
        self.pushButtonDeregister.setText(QCoreApplication.translate("RegisterDialog", u"&Deregister", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.registerTab), QCoreApplication.translate("RegisterDialog", u"Register", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("RegisterDialog", u"Settings", None))
    # retranslateUi

