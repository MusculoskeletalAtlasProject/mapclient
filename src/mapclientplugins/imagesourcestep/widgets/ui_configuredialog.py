# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(629, 581)
        self.verticalLayout_2 = QVBoxLayout(ConfigureDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(ConfigureDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.localTab = QWidget()
        self.localTab.setObjectName(u"localTab")
        self.gridLayout = QGridLayout(self.localTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.localTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(71, 0))

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.localButton = QPushButton(self.localTab)
        self.localButton.setObjectName(u"localButton")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.localButton.setFont(font)

        self.gridLayout.addWidget(self.localButton, 0, 3, 1, 1)

        self.localLineEdit = QLineEdit(self.localTab)
        self.localLineEdit.setObjectName(u"localLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localLineEdit.sizePolicy().hasHeightForWidth())
        self.localLineEdit.setSizePolicy(sizePolicy)
        self.localLineEdit.setStyleSheet(u"selection-color: red;\n"
"color: green")

        self.gridLayout.addWidget(self.localLineEdit, 0, 1, 1, 2)

        self.previousLocationLabel = QLabel(self.localTab)
        self.previousLocationLabel.setObjectName(u"previousLocationLabel")
        self.previousLocationLabel.setMaximumSize(QSize(0, 16777215))

        self.gridLayout.addWidget(self.previousLocationLabel, 1, 2, 1, 1)

        self.tabWidget.addTab(self.localTab, "")
        self.pmrTab = QWidget()
        self.pmrTab.setObjectName(u"pmrTab")
        self.verticalLayout_4 = QVBoxLayout(self.pmrTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget.addTab(self.pmrTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.imageSourceTypeComboBox = QComboBox(self.groupBox)
        self.imageSourceTypeComboBox.addItem("")
        self.imageSourceTypeComboBox.addItem("")
        self.imageSourceTypeComboBox.addItem("")
        self.imageSourceTypeComboBox.addItem("")
        self.imageSourceTypeComboBox.addItem("")
        self.imageSourceTypeComboBox.setObjectName(u"imageSourceTypeComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imageSourceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.imageSourceTypeComboBox.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.imageSourceTypeComboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label_3.setBuddy(self.localLineEdit)
        self.label_6.setBuddy(self.imageSourceTypeComboBox)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure - Image Source", None))
        self.groupBox.setTitle("")
        self.label_3.setText(QCoreApplication.translate("ConfigureDialog", u"Location:", None))
        self.localButton.setText(QCoreApplication.translate("ConfigureDialog", u"...", None))
        self.previousLocationLabel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.localTab), QCoreApplication.translate("ConfigureDialog", u"Local file system", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pmrTab), QCoreApplication.translate("ConfigureDialog", u"Physiome Model Repository", None))
        self.label_6.setText(QCoreApplication.translate("ConfigureDialog", u"Image Source Type:", None))
        self.imageSourceTypeComboBox.setItemText(0, QCoreApplication.translate("ConfigureDialog", u"from file extension", None))
        self.imageSourceTypeComboBox.setItemText(1, QCoreApplication.translate("ConfigureDialog", u"png (*.png)", None))
        self.imageSourceTypeComboBox.setItemText(2, QCoreApplication.translate("ConfigureDialog", u"jpg (*.jpg, *.jpeg)", None))
        self.imageSourceTypeComboBox.setItemText(3, QCoreApplication.translate("ConfigureDialog", u"TIFF (*.tiff)", None))
        self.imageSourceTypeComboBox.setItemText(4, QCoreApplication.translate("ConfigureDialog", u"DICOM (*.dcm)", None))

    # retranslateUi

