# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downloadtodirectorydialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DownloadToDirectoryDialog(object):
    def setupUi(self, DownloadToDirectoryDialog):
        if not DownloadToDirectoryDialog.objectName():
            DownloadToDirectoryDialog.setObjectName(u"DownloadToDirectoryDialog")
        DownloadToDirectoryDialog.resize(491, 153)
        self.verticalLayout = QVBoxLayout(DownloadToDirectoryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(DownloadToDirectoryDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBoxDirChooser = QComboBox(self.groupBox)
        self.comboBoxDirChooser.setObjectName(u"comboBoxDirChooser")

        self.horizontalLayout.addWidget(self.comboBoxDirChooser)

        self.pushButtonDirChooser = QPushButton(self.groupBox)
        self.pushButtonDirChooser.setObjectName(u"pushButtonDirChooser")
        self.pushButtonDirChooser.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonDirChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonDownload = QPushButton(DownloadToDirectoryDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout_2.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonCancel = QPushButton(DownloadToDirectoryDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_2.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.pushButtonDirChooser, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonCancel)

        self.retranslateUi(DownloadToDirectoryDialog)
        self.pushButtonCancel.clicked.connect(DownloadToDirectoryDialog.reject)

        QMetaObject.connectSlotsByName(DownloadToDirectoryDialog)
    # setupUi

    def retranslateUi(self, DownloadToDirectoryDialog):
        DownloadToDirectoryDialog.setWindowTitle(QCoreApplication.translate("DownloadToDirectoryDialog", u"Update Workflow Tool", None))
        self.groupBox.setTitle("")
        self.label_4.setText(QCoreApplication.translate("DownloadToDirectoryDialog", u"Select directory to download plugin(s) to:", None))
#if QT_CONFIG(tooltip)
        self.pushButtonDirChooser.setToolTip(QCoreApplication.translate("DownloadToDirectoryDialog", u"Choose workflow directory to update", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonDirChooser.setText(QCoreApplication.translate("DownloadToDirectoryDialog", u"...", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("DownloadToDirectoryDialog", u"Download", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DownloadToDirectoryDialog", u"Cancel", None))
    # retranslateUi

