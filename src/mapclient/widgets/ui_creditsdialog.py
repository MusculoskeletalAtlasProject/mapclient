# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/creditsdialog.ui'
#
# Created: Fri Jun 14 11:25:25 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CreditsDialog(object):
    def setupUi(self, CreditsDialog):
        CreditsDialog.setObjectName("CreditsDialog")
        CreditsDialog.resize(475, 356)
        self.verticalLayout = QtGui.QVBoxLayout(CreditsDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_CreditsTab = QtGui.QFrame(CreditsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_CreditsTab.sizePolicy().hasHeightForWidth())
        self.frame_CreditsTab.setSizePolicy(sizePolicy)
        self.frame_CreditsTab.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_CreditsTab.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_CreditsTab.setObjectName("frame_CreditsTab")
        self.verticalLayout.addWidget(self.frame_CreditsTab)
        self.frame = QtGui.QFrame(CreditsDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_Close = QtGui.QPushButton(self.frame)
        self.btn_Close.setObjectName("btn_Close")
        self.horizontalLayout.addWidget(self.btn_Close)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(CreditsDialog)
        QtCore.QObject.connect(self.btn_Close, QtCore.SIGNAL("clicked()"), CreditsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(CreditsDialog)

    def retranslateUi(self, CreditsDialog):
        CreditsDialog.setWindowTitle(QtGui.QApplication.translate("CreditsDialog", "MAP Client Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Close.setText(QtGui.QApplication.translate("CreditsDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

