# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importworkflowdialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ImportWorkflowDialog(object):
    def setupUi(self, ImportWorkflowDialog):
        if not ImportWorkflowDialog.objectName():
            ImportWorkflowDialog.setObjectName(u"ImportWorkflowDialog")
        ImportWorkflowDialog.resize(541, 523)
        self.verticalLayout = QVBoxLayout(ImportWorkflowDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(ImportWorkflowDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditLocation = QLineEdit(ImportWorkflowDialog)
        self.lineEditLocation.setObjectName(u"lineEditLocation")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLocation.sizePolicy().hasHeightForWidth())
        self.lineEditLocation.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lineEditLocation)

        self.pushButtonLocation = QPushButton(ImportWorkflowDialog)
        self.pushButtonLocation.setObjectName(u"pushButtonLocation")

        self.horizontalLayout.addWidget(self.pushButtonLocation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBoxImport = QDialogButtonBox(ImportWorkflowDialog)
        self.buttonBoxImport.setObjectName(u"buttonBoxImport")
        self.buttonBoxImport.setOrientation(Qt.Horizontal)
        self.buttonBoxImport.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBoxImport)


        self.retranslateUi(ImportWorkflowDialog)
        self.buttonBoxImport.accepted.connect(ImportWorkflowDialog.accept)
        self.buttonBoxImport.rejected.connect(ImportWorkflowDialog.reject)

        QMetaObject.connectSlotsByName(ImportWorkflowDialog)
    # setupUi

    def retranslateUi(self, ImportWorkflowDialog):
        ImportWorkflowDialog.setWindowTitle(QCoreApplication.translate("ImportWorkflowDialog", u"Import Workflow", None))
        self.label.setText(QCoreApplication.translate("ImportWorkflowDialog", u"Destination:", None))
        self.pushButtonLocation.setText(QCoreApplication.translate("ImportWorkflowDialog", u"...", None))
    # retranslateUi

