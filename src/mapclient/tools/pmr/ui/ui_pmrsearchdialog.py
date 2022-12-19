# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmrsearchdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PMRSearchDialog(object):
    def setupUi(self, PMRSearchDialog):
        if not PMRSearchDialog.objectName():
            PMRSearchDialog.setObjectName(u"PMRSearchDialog")
        PMRSearchDialog.resize(387, 493)
        self.gridLayout_2 = QGridLayout(PMRSearchDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.loginHorizontalLayout = QHBoxLayout()
        self.loginHorizontalLayout.setObjectName(u"loginHorizontalLayout")
        self.label = QLabel(PMRSearchDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.loginHorizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.loginHorizontalLayout.addItem(self.horizontalSpacer)

        self.loginStackedWidget = QStackedWidget(PMRSearchDialog)
        self.loginStackedWidget.setObjectName(u"loginStackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.loginStackedWidget.sizePolicy().hasHeightForWidth())
        self.loginStackedWidget.setSizePolicy(sizePolicy1)
        self.loginStackedWidget.setMaximumSize(QSize(16777215, 40))
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.horizontalLayout = QHBoxLayout(self.loginPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.registerLabel = QLabel(self.loginPage)
        self.registerLabel.setObjectName(u"registerLabel")
        font = QFont()
        font.setPointSize(7)
        self.registerLabel.setFont(font)
        self.registerLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.registerLabel)

        self.loginStackedWidget.addWidget(self.loginPage)
        self.logoutPage = QWidget()
        self.logoutPage.setObjectName(u"logoutPage")
        self.horizontalLayout_2 = QHBoxLayout(self.logoutPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.deregisterLabel = QLabel(self.logoutPage)
        self.deregisterLabel.setObjectName(u"deregisterLabel")
        self.deregisterLabel.setFont(font)
        self.deregisterLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.deregisterLabel)

        self.loginStackedWidget.addWidget(self.logoutPage)

        self.loginHorizontalLayout.addWidget(self.loginStackedWidget)


        self.verticalLayout.addLayout(self.loginHorizontalLayout)

        self.pmrGroupBox = QGroupBox(PMRSearchDialog)
        self.pmrGroupBox.setObjectName(u"pmrGroupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.pmrGroupBox.sizePolicy().hasHeightForWidth())
        self.pmrGroupBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.pmrGroupBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.searchLineEdit = QLineEdit(self.pmrGroupBox)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout_3.addWidget(self.searchLineEdit)

        self.searchButton = QPushButton(self.pmrGroupBox)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_3.addWidget(self.searchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.label_2 = QLabel(self.pmrGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.searchResultsListWidget = QListWidget(self.pmrGroupBox)
        self.searchResultsListWidget.setObjectName(u"searchResultsListWidget")

        self.verticalLayout_2.addWidget(self.searchResultsListWidget)


        self.verticalLayout.addWidget(self.pmrGroupBox)

        self.buttonBox = QDialogButtonBox(PMRSearchDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.searchLineEdit, self.searchButton)
        QWidget.setTabOrder(self.searchButton, self.searchResultsListWidget)
        QWidget.setTabOrder(self.searchResultsListWidget, self.buttonBox)

        self.retranslateUi(PMRSearchDialog)
        self.buttonBox.accepted.connect(PMRSearchDialog.accept)
        self.buttonBox.rejected.connect(PMRSearchDialog.reject)

        self.loginStackedWidget.setCurrentIndex(0)
        self.searchButton.setDefault(True)


        QMetaObject.connectSlotsByName(PMRSearchDialog)
    # setupUi

    def retranslateUi(self, PMRSearchDialog):
        PMRSearchDialog.setWindowTitle(QCoreApplication.translate("PMRSearchDialog", u"Physiome Model Repository", None))
        self.label.setText(QCoreApplication.translate("PMRSearchDialog", u"Physiome Model Repository", None))
        self.registerLabel.setText(QCoreApplication.translate("PMRSearchDialog", u"<a href=\"mapclient.register\">register</a>", None))
        self.deregisterLabel.setText(QCoreApplication.translate("PMRSearchDialog", u"<a href=\"http://mapclient.logout\">deregister</a>", None))
        self.pmrGroupBox.setTitle("")
        self.searchButton.setText(QCoreApplication.translate("PMRSearchDialog", u"Search", None))
        self.label_2.setText(QCoreApplication.translate("PMRSearchDialog", u"Search results:", None))
    # retranslateUi

