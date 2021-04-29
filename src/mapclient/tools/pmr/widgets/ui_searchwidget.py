# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        if not SearchWidget.objectName():
            SearchWidget.setObjectName(u"SearchWidget")
        SearchWidget.resize(466, 480)
        self.verticalLayout = QVBoxLayout(SearchWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.searchLineEdit = QLineEdit(SearchWidget)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout_3.addWidget(self.searchLineEdit)

        self.searchButton = QPushButton(SearchWidget)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_3.addWidget(self.searchButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_2 = QLabel(SearchWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.searchResultsListWidget = QListWidget(SearchWidget)
        self.searchResultsListWidget.setObjectName(u"searchResultsListWidget")

        self.verticalLayout.addWidget(self.searchResultsListWidget)

        self.label_3 = QLabel(SearchWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.targetEdit = QLineEdit(SearchWidget)
        self.targetEdit.setObjectName(u"targetEdit")

        self.verticalLayout.addWidget(self.targetEdit)


        self.retranslateUi(SearchWidget)

        self.searchButton.setDefault(True)


        QMetaObject.connectSlotsByName(SearchWidget)
    # setupUi

    def retranslateUi(self, SearchWidget):
        SearchWidget.setWindowTitle(QCoreApplication.translate("SearchWidget", u"Search", None))
        self.searchButton.setText(QCoreApplication.translate("SearchWidget", u"Search", None))
        self.label_2.setText(QCoreApplication.translate("SearchWidget", u"Search results:", None))
        self.label_3.setText(QCoreApplication.translate("SearchWidget", u"Result target:", None))
    # retranslateUi

