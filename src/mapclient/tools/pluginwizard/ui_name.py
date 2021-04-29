# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'name.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_Name(object):
    def setupUi(self, Name):
        if not Name.objectName():
            Name.setObjectName(u"Name")
        Name.resize(498, 296)
        self.gridLayout = QGridLayout(Name)
        self.gridLayout.setObjectName(u"gridLayout")
        self.nameLineEdit = QLineEdit(Name)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setEnabled(True)

        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)

        self.packageNameLineEdit = QLineEdit(Name)
        self.packageNameLineEdit.setObjectName(u"packageNameLineEdit")

        self.gridLayout.addWidget(self.packageNameLineEdit, 1, 1, 1, 1)

        self.iconButton = QPushButton(Name)
        self.iconButton.setObjectName(u"iconButton")

        self.gridLayout.addWidget(self.iconButton, 2, 2, 1, 1)

        self.iconLabel = QLabel(Name)
        self.iconLabel.setObjectName(u"iconLabel")

        self.gridLayout.addWidget(self.iconLabel, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 1)

        self.nameLabel = QLabel(Name)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.iconLineEdit = QLineEdit(Name)
        self.iconLineEdit.setObjectName(u"iconLineEdit")

        self.gridLayout.addWidget(self.iconLineEdit, 2, 1, 1, 1)

        self.packageNameLabel = QLabel(Name)
        self.packageNameLabel.setObjectName(u"packageNameLabel")

        self.gridLayout.addWidget(self.packageNameLabel, 1, 0, 1, 1)

        self.frame = QFrame(Name)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 72))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(u"QFrame {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 aliceblue, stop:1 lightskyblue);}\n"
"QLabel {background-color: transparent}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.iconPictureLabel = QLabel(self.frame)
        self.iconPictureLabel.setObjectName(u"iconPictureLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconPictureLabel.sizePolicy().hasHeightForWidth())
        self.iconPictureLabel.setSizePolicy(sizePolicy)
        self.iconPictureLabel.setMinimumSize(QSize(64, 64))
        self.iconPictureLabel.setMaximumSize(QSize(64, 64))
        self.iconPictureLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.iconPictureLabel, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 5, 1, 1, 1)

        self.label = QLabel(Name)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.label_2 = QLabel(Name)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.comboBoxPresetIcons = QComboBox(Name)
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.addItem("")
        self.comboBoxPresetIcons.setObjectName(u"comboBoxPresetIcons")

        self.gridLayout.addWidget(self.comboBoxPresetIcons, 4, 1, 1, 1)

#if QT_CONFIG(shortcut)
        self.iconLabel.setBuddy(self.nameLineEdit)
        self.nameLabel.setBuddy(self.iconLineEdit)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Name)

        QMetaObject.connectSlotsByName(Name)
    # setupUi

    def retranslateUi(self, Name):
        Name.setWindowTitle(QCoreApplication.translate("Name", u"Form", None))
#if QT_CONFIG(tooltip)
        self.nameLineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.iconButton.setText(QCoreApplication.translate("Name", u"...", None))
        self.iconLabel.setText(QCoreApplication.translate("Name", u"Icon from fi&le:", None))
        self.nameLabel.setText(QCoreApplication.translate("Name", u"Step &Name:", None))
        self.packageNameLabel.setText(QCoreApplication.translate("Name", u"Package Name:  ", None))
        self.iconPictureLabel.setText(QCoreApplication.translate("Name", u"Icon", None))
        self.label.setText(QCoreApplication.translate("Name", u"or", None))
        self.label_2.setText(QCoreApplication.translate("Name", u"Preset Icon:", None))
        self.comboBoxPresetIcons.setItemText(0, QCoreApplication.translate("Name", u"Default", None))
        self.comboBoxPresetIcons.setItemText(1, QCoreApplication.translate("Name", u"Source", None))
        self.comboBoxPresetIcons.setItemText(2, QCoreApplication.translate("Name", u"Sink", None))
        self.comboBoxPresetIcons.setItemText(3, QCoreApplication.translate("Name", u"Fitting", None))
        self.comboBoxPresetIcons.setItemText(4, QCoreApplication.translate("Name", u"Model Viewer", None))
        self.comboBoxPresetIcons.setItemText(5, QCoreApplication.translate("Name", u"Image Processing", None))
        self.comboBoxPresetIcons.setItemText(6, QCoreApplication.translate("Name", u"Segmentation", None))
        self.comboBoxPresetIcons.setItemText(7, QCoreApplication.translate("Name", u"Morphometric", None))
        self.comboBoxPresetIcons.setItemText(8, QCoreApplication.translate("Name", u"Registration", None))
        self.comboBoxPresetIcons.setItemText(9, QCoreApplication.translate("Name", u"Utility", None))

#if QT_CONFIG(tooltip)
        self.comboBoxPresetIcons.setToolTip(QCoreApplication.translate("Name", u"Icon from file is used if a valid icon file is defined", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

