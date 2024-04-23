# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'packagemanagerdialog.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
class Ui_PackageManagerDialog(object):
    def setupUi(self, PackageManagerDialog):
        if not PackageManagerDialog.objectName():
            PackageManagerDialog.setObjectName(u"PackageManagerDialog")
        PackageManagerDialog.resize(567, 496)
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        PackageManagerDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PackageManagerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(PackageManagerDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.directoryListing = QListWidget(self.groupBox)
        self.directoryListing.setObjectName(u"directoryListing")

        self.verticalLayout_3.addWidget(self.directoryListing)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.addButton = QPushButton(self.groupBox)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout_2.addWidget(self.addButton)

        self.removeButton = QPushButton(self.groupBox)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout_2.addWidget(self.removeButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(PackageManagerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(PackageManagerDialog)
        self.buttonBox.rejected.connect(PackageManagerDialog.reject)
        self.buttonBox.accepted.connect(PackageManagerDialog.accept)

        QMetaObject.connectSlotsByName(PackageManagerDialog)
    # setupUi

    def retranslateUi(self, PackageManagerDialog):
        PackageManagerDialog.setWindowTitle(QCoreApplication.translate("PackageManagerDialog", u"Package Manager", None))
        self.groupBox.setTitle(QCoreApplication.translate("PackageManagerDialog", u"Package Manager", None))
        self.label.setText(QCoreApplication.translate("PackageManagerDialog", u"Package directories:", None))
        self.addButton.setText(QCoreApplication.translate("PackageManagerDialog", u"Add Directory", None))
        self.removeButton.setText(QCoreApplication.translate("PackageManagerDialog", u"Remove Directory", None))
    # retranslateUi

