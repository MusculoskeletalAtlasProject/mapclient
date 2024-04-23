# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmrworkflowwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_PMRWorkflowWidget(object):
    def setupUi(self, PMRWorkflowWidget):
        if not PMRWorkflowWidget.objectName():
            PMRWorkflowWidget.setObjectName(u"PMRWorkflowWidget")
        PMRWorkflowWidget.resize(791, 711)
        self.verticalLayout_2 = QVBoxLayout(PMRWorkflowWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.labelLink = QLabel(PMRWorkflowWidget)
        self.labelLink.setObjectName(u"labelLink")

        self.gridLayout.addWidget(self.labelLink, 0, 1, 1, 1)

        self.groupBox = QGroupBox(PMRWorkflowWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBoxSearch = QComboBox(self.groupBox)
        self.comboBoxSearch.addItem("")
        self.comboBoxSearch.addItem("")
        self.comboBoxSearch.setObjectName(u"comboBoxSearch")

        self.horizontalLayout_2.addWidget(self.comboBoxSearch)

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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditWorkspace = QLineEdit(self.groupBox)
        self.lineEditWorkspace.setObjectName(u"lineEditWorkspace")
        self.lineEditWorkspace.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEditWorkspace)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonImport = QPushButton(PMRWorkflowWidget)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout_3.addWidget(self.pushButtonImport)

        self.pushButtonExport = QPushButton(PMRWorkflowWidget)
        self.pushButtonExport.setObjectName(u"pushButtonExport")

        self.horizontalLayout_3.addWidget(self.pushButtonExport)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.lineEditWorkspace)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(PMRWorkflowWidget)

        QMetaObject.connectSlotsByName(PMRWorkflowWidget)
    # setupUi

    def retranslateUi(self, PMRWorkflowWidget):
        PMRWorkflowWidget.setWindowTitle(QCoreApplication.translate("PMRWorkflowWidget", u"PMR Workflow Tool", None))
        self.labelLink.setText(QCoreApplication.translate("PMRWorkflowWidget", u"<a href=\"mapclient.register\">register</a>", None))
        self.groupBox.setTitle(QCoreApplication.translate("PMRWorkflowWidget", u"Physiome Model Repository", None))
        self.comboBoxSearch.setItemText(0, QCoreApplication.translate("PMRWorkflowWidget", u"Ontological term", None))
        self.comboBoxSearch.setItemText(1, QCoreApplication.translate("PMRWorkflowWidget", u"Plain text", None))

        self.pushButtonSearch.setText(QCoreApplication.translate("PMRWorkflowWidget", u"&Search", None))
        self.label.setText(QCoreApplication.translate("PMRWorkflowWidget", u"Workspace:", None))
#if QT_CONFIG(tooltip)
        self.pushButtonImport.setToolTip(QCoreApplication.translate("PMRWorkflowWidget", u"Import to local location", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonImport.setText(QCoreApplication.translate("PMRWorkflowWidget", u"Import", None))
#if QT_CONFIG(tooltip)
        self.pushButtonExport.setToolTip(QCoreApplication.translate("PMRWorkflowWidget", u"Export from local location", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonExport.setText(QCoreApplication.translate("PMRWorkflowWidget", u"Export", None))
    # retranslateUi

