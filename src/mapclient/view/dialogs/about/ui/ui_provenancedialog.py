# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'provenancedialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ProvenanceDialog(object):
    def setupUi(self, ProvenanceDialog):
        if not ProvenanceDialog.objectName():
            ProvenanceDialog.setObjectName(u"ProvenanceDialog")
        ProvenanceDialog.resize(575, 556)
        self.verticalLayout = QVBoxLayout(ProvenanceDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(ProvenanceDialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxMAPClient = QGroupBox(self.frame_2)
        self.groupBoxMAPClient.setObjectName(u"groupBoxMAPClient")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxMAPClient)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableWidgetMAPClient = QTableWidget(self.groupBoxMAPClient)
        self.tableWidgetMAPClient.setObjectName(u"tableWidgetMAPClient")
        self.tableWidgetMAPClient.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetMAPClient.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.tableWidgetMAPClient)


        self.verticalLayout_2.addWidget(self.groupBoxMAPClient)

        self.groupBoxPlugin = QGroupBox(self.frame_2)
        self.groupBoxPlugin.setObjectName(u"groupBoxPlugin")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxPlugin)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableWidgetPlugin = QTableWidget(self.groupBoxPlugin)
        self.tableWidgetPlugin.setObjectName(u"tableWidgetPlugin")

        self.verticalLayout_4.addWidget(self.tableWidgetPlugin)


        self.verticalLayout_2.addWidget(self.groupBoxPlugin)

        self.groupBoxPackage = QGroupBox(self.frame_2)
        self.groupBoxPackage.setObjectName(u"groupBoxPackage")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxPackage)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableWidgetPackage = QTableWidget(self.groupBoxPackage)
        self.tableWidgetPackage.setObjectName(u"tableWidgetPackage")

        self.verticalLayout_5.addWidget(self.tableWidgetPackage)


        self.verticalLayout_2.addWidget(self.groupBoxPackage)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(ProvenanceDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_Close = QPushButton(self.frame)
        self.btn_Close.setObjectName(u"btn_Close")

        self.horizontalLayout.addWidget(self.btn_Close)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(ProvenanceDialog)
        self.btn_Close.clicked.connect(ProvenanceDialog.close)

        QMetaObject.connectSlotsByName(ProvenanceDialog)
    # setupUi

    def retranslateUi(self, ProvenanceDialog):
        ProvenanceDialog.setWindowTitle(QCoreApplication.translate("ProvenanceDialog", u"MAP Client Provenance", None))
        self.groupBoxMAPClient.setTitle(QCoreApplication.translate("ProvenanceDialog", u"MAP Client provenance", None))
        self.groupBoxPlugin.setTitle(QCoreApplication.translate("ProvenanceDialog", u"Plugin provenance", None))
        self.groupBoxPackage.setTitle(QCoreApplication.translate("ProvenanceDialog", u"Package provenance", None))
        self.btn_Close.setText(QCoreApplication.translate("ProvenanceDialog", u"&Close", None))
    # retranslateUi

