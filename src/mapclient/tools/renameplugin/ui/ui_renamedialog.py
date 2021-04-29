# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'renamedialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        if not RenameDialog.objectName():
            RenameDialog.setObjectName(u"RenameDialog")
        RenameDialog.resize(491, 357)
        self.verticalLayout = QVBoxLayout(RenameDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(RenameDialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
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
        self.lineEditStepLocation = QLineEdit(self.groupBox)
        self.lineEditStepLocation.setObjectName(u"lineEditStepLocation")

        self.horizontalLayout.addWidget(self.lineEditStepLocation)

        self.pushButtonStepChooser = QPushButton(self.groupBox)
        self.pushButtonStepChooser.setObjectName(u"pushButtonStepChooser")

        self.horizontalLayout.addWidget(self.pushButtonStepChooser)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)

        self.lineEditRenamePackageFrom = QLineEdit(self.groupBox)
        self.lineEditRenamePackageFrom.setObjectName(u"lineEditRenamePackageFrom")
        self.lineEditRenamePackageFrom.setEnabled(False)
        self.lineEditRenamePackageFrom.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRenamePackageFrom, 1, 1, 1, 1)

        self.lineEditRenamePackageTo = QLineEdit(self.groupBox)
        self.lineEditRenamePackageTo.setObjectName(u"lineEditRenamePackageTo")

        self.gridLayout.addWidget(self.lineEditRenamePackageTo, 1, 3, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.lineEditRenameStepTo = QLineEdit(self.groupBox)
        self.lineEditRenameStepTo.setObjectName(u"lineEditRenameStepTo")

        self.gridLayout.addWidget(self.lineEditRenameStepTo, 0, 3, 1, 1)

        self.lineEditRenameStepFrom = QLineEdit(self.groupBox)
        self.lineEditRenameStepFrom.setObjectName(u"lineEditRenameStepFrom")
        self.lineEditRenameStepFrom.setEnabled(False)
        self.lineEditRenameStepFrom.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRenameStepFrom, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.treeWidgetRename = QTreeWidget(self.groupBox)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidgetRename.setHeaderItem(__qtreewidgetitem)
        self.treeWidgetRename.setObjectName(u"treeWidgetRename")
        self.treeWidgetRename.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeWidgetRename.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.treeWidgetRename)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonRename = QPushButton(RenameDialog)
        self.pushButtonRename.setObjectName(u"pushButtonRename")

        self.horizontalLayout_2.addWidget(self.pushButtonRename)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonCancel = QPushButton(RenameDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_2.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.lineEditStepLocation, self.pushButtonStepChooser)
        QWidget.setTabOrder(self.pushButtonStepChooser, self.lineEditRenameStepFrom)
        QWidget.setTabOrder(self.lineEditRenameStepFrom, self.lineEditRenameStepTo)
        QWidget.setTabOrder(self.lineEditRenameStepTo, self.lineEditRenamePackageFrom)
        QWidget.setTabOrder(self.lineEditRenamePackageFrom, self.lineEditRenamePackageTo)
        QWidget.setTabOrder(self.lineEditRenamePackageTo, self.treeWidgetRename)
        QWidget.setTabOrder(self.treeWidgetRename, self.pushButtonRename)
        QWidget.setTabOrder(self.pushButtonRename, self.pushButtonCancel)

        self.retranslateUi(RenameDialog)
        self.pushButtonCancel.clicked.connect(RenameDialog.reject)

        QMetaObject.connectSlotsByName(RenameDialog)
    # setupUi

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QCoreApplication.translate("RenameDialog", u"Rename Step Tool", None))
        self.groupBox.setTitle("")
        self.label_4.setText(QCoreApplication.translate("RenameDialog", u"Step to rename (location on disk):", None))
        self.pushButtonStepChooser.setText(QCoreApplication.translate("RenameDialog", u"...", None))
        self.label_9.setText(QCoreApplication.translate("RenameDialog", u" to:", None))
        self.label_10.setText(QCoreApplication.translate("RenameDialog", u"Rename Package name from:", None))
        self.label.setText(QCoreApplication.translate("RenameDialog", u"Rename Step name from:", None))
        self.label_3.setText(QCoreApplication.translate("RenameDialog", u" to:", None))
        self.pushButtonRename.setText(QCoreApplication.translate("RenameDialog", u"Rename", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("RenameDialog", u"Cancel", None))
    # retranslateUi

