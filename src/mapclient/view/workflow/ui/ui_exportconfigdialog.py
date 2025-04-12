# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportconfigdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ExportConfigDialog(object):
    def setupUi(self, ExportConfigDialog):
        if not ExportConfigDialog.objectName():
            ExportConfigDialog.setObjectName(u"ExportConfigDialog")
        ExportConfigDialog.resize(562, 459)
        self.verticalLayout = QVBoxLayout(ExportConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.exportToLabel = QLabel(ExportConfigDialog)
        self.exportToLabel.setObjectName(u"exportToLabel")

        self.horizontalLayout.addWidget(self.exportToLabel)

        self.exportToLineEdit = QLineEdit(ExportConfigDialog)
        self.exportToLineEdit.setObjectName(u"exportToLineEdit")

        self.horizontalLayout.addWidget(self.exportToLineEdit)

        self.exportToButton = QPushButton(ExportConfigDialog)
        self.exportToButton.setObjectName(u"exportToButton")

        self.horizontalLayout.addWidget(self.exportToButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(ExportConfigDialog)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.selectAllButton = QPushButton(ExportConfigDialog)
        self.selectAllButton.setObjectName(u"selectAllButton")

        self.buttonLayout.addWidget(self.selectAllButton)

        self.deselectAllButton = QPushButton(ExportConfigDialog)
        self.deselectAllButton.setObjectName(u"deselectAllButton")

        self.buttonLayout.addWidget(self.deselectAllButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.exportButton = QPushButton(ExportConfigDialog)
        self.exportButton.setObjectName(u"exportButton")

        self.buttonLayout.addWidget(self.exportButton)

        self.cancelButton = QPushButton(ExportConfigDialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.buttonLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(ExportConfigDialog)
        self.cancelButton.clicked.connect(ExportConfigDialog.reject)

        QMetaObject.connectSlotsByName(ExportConfigDialog)
    # setupUi

    def retranslateUi(self, ExportConfigDialog):
        ExportConfigDialog.setWindowTitle(QCoreApplication.translate("ExportConfigDialog", u"Select Important Items", None))
        self.exportToLabel.setText(QCoreApplication.translate("ExportConfigDialog", u"Export to:", None))
        self.exportToButton.setText(QCoreApplication.translate("ExportConfigDialog", u"...", None))
        self.selectAllButton.setText(QCoreApplication.translate("ExportConfigDialog", u"Select All", None))
        self.deselectAllButton.setText(QCoreApplication.translate("ExportConfigDialog", u"Deselect All", None))
        self.exportButton.setText(QCoreApplication.translate("ExportConfigDialog", u"Export", None))
        self.cancelButton.setText(QCoreApplication.translate("ExportConfigDialog", u"Cancel", None))
    # retranslateUi

