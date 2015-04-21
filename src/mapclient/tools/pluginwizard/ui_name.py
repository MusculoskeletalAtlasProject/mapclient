# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/name.ui'
#
# Created: Thu Oct 17 11:02:13 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Name(object):
    def setupUi(self, Name):
        Name.setObjectName("Name")
        Name.resize(498, 296)
        self.gridLayout = QtGui.QGridLayout(Name)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLineEdit = QtGui.QLineEdit(Name)
        self.nameLineEdit.setEnabled(True)
        self.nameLineEdit.setToolTip("")
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.packageNameLineEdit = QtGui.QLineEdit(Name)
        self.packageNameLineEdit.setObjectName("packageNameLineEdit")
        self.gridLayout.addWidget(self.packageNameLineEdit, 1, 1, 1, 1)
        self.iconButton = QtGui.QPushButton(Name)
        self.iconButton.setObjectName("iconButton")
        self.gridLayout.addWidget(self.iconButton, 2, 2, 1, 1)
        self.iconLabel = QtGui.QLabel(Name)
        self.iconLabel.setObjectName("iconLabel")
        self.gridLayout.addWidget(self.iconLabel, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.nameLabel = QtGui.QLabel(Name)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.iconLineEdit = QtGui.QLineEdit(Name)
        self.iconLineEdit.setObjectName("iconLineEdit")
        self.gridLayout.addWidget(self.iconLineEdit, 2, 1, 1, 1)
        self.packageNameLabel = QtGui.QLabel(Name)
        self.packageNameLabel.setObjectName("packageNameLabel")
        self.gridLayout.addWidget(self.packageNameLabel, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(Name)
        self.frame.setMinimumSize(QtCore.QSize(0, 72))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("QFrame {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 aliceblue, stop:1 lightskyblue);}\n"
"QLabel {background-color: transparent}")
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.iconPictureLabel = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconPictureLabel.sizePolicy().hasHeightForWidth())
        self.iconPictureLabel.setSizePolicy(sizePolicy)
        self.iconPictureLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.iconPictureLabel.setMaximumSize(QtCore.QSize(64, 64))
        self.iconPictureLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconPictureLabel.setObjectName("iconPictureLabel")
        self.gridLayout_2.addWidget(self.iconPictureLabel, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 3, 1, 1, 1)
        self.iconLabel.setBuddy(self.nameLineEdit)
        self.nameLabel.setBuddy(self.iconLineEdit)

        self.retranslateUi(Name)
        QtCore.QMetaObject.connectSlotsByName(Name)

    def retranslateUi(self, Name):
        Name.setWindowTitle(QtGui.QApplication.translate("Name", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.iconButton.setText(QtGui.QApplication.translate("Name", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.iconLabel.setText(QtGui.QApplication.translate("Name", "Icon:", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("Name", "Step Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.packageNameLabel.setText(QtGui.QApplication.translate("Name", "Package Name:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.iconPictureLabel.setText(QtGui.QApplication.translate("Name", "Icon", None, QtGui.QApplication.UnicodeUTF8))

