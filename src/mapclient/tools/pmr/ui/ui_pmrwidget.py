# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmrwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PMRWidget(object):
    def setupUi(self, PMRWidget):
        if not PMRWidget.objectName():
            PMRWidget.setObjectName(u"PMRWidget")
        PMRWidget.resize(614, 602)
        self.verticalLayout_2 = QVBoxLayout(PMRWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(PMRWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.groupBox = QGroupBox(PMRWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditLocation = QLineEdit(self.groupBox)
        self.lineEditLocation.setObjectName(u"lineEditLocation")

        self.horizontalLayout.addWidget(self.lineEditLocation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditSearch = QLineEdit(self.groupBox)
        self.lineEditSearch.setObjectName(u"lineEditSearch")

        self.horizontalLayout_2.addWidget(self.lineEditSearch)

        self.pushButtonSearch = QPushButton(self.groupBox)
        self.pushButtonSearch.setObjectName(u"pushButtonSearch")

        self.horizontalLayout_2.addWidget(self.pushButtonSearch)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listWidgetResults = QListWidget(self.groupBox)
        self.listWidgetResults.setObjectName(u"listWidgetResults")

        self.verticalLayout.addWidget(self.listWidgetResults)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonImport = QPushButton(PMRWidget)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout_3.addWidget(self.pushButtonImport)

        self.pushButtonExport = QPushButton(PMRWidget)
        self.pushButtonExport.setObjectName(u"pushButtonExport")

        self.horizontalLayout_3.addWidget(self.pushButtonExport)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(PMRWidget)

        QMetaObject.connectSlotsByName(PMRWidget)
    # setupUi

    def retranslateUi(self, PMRWidget):
        PMRWidget.setWindowTitle(QCoreApplication.translate("PMRWidget", u"PMR Workflow Tool", None))
        self.label_2.setText(QCoreApplication.translate("PMRWidget", u"<a href=\"mapclient.register\">register</a>", None))
        self.groupBox.setTitle(QCoreApplication.translate("PMRWidget", u"Physiome Model Repository", None))
        self.label.setText(QCoreApplication.translate("PMRWidget", u"Location:", None))
        self.pushButtonSearch.setText(QCoreApplication.translate("PMRWidget", u"&Search", None))
#if QT_CONFIG(tooltip)
        self.pushButtonImport.setToolTip(QCoreApplication.translate("PMRWidget", u"Import to local location", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonImport.setText(QCoreApplication.translate("PMRWidget", u"Import", None))
#if QT_CONFIG(tooltip)
        self.pushButtonExport.setToolTip(QCoreApplication.translate("PMRWidget", u"Export from local location", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonExport.setText(QCoreApplication.translate("PMRWidget", u"Export", None))
    # retranslateUi

