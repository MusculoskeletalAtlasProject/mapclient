# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/checkstatusdialog.ui'
#
# Created: Wed Jul  1 16:13:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CheckStatusDialog(object):
    def setupUi(self, CheckStatusDialog):
        CheckStatusDialog.setObjectName("CheckStatusDialog")
        CheckStatusDialog.resize(548, 284)
        self.verticalLayout = QtGui.QVBoxLayout(CheckStatusDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(CheckStatusDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.labelCheckTitle = QtGui.QLabel(CheckStatusDialog)
        self.labelCheckTitle.setObjectName("labelCheckTitle")
        self.horizontalLayout.addWidget(self.labelCheckTitle)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plainTextEditScreen = QtGui.QPlainTextEdit(CheckStatusDialog)
        self.plainTextEditScreen.setObjectName("plainTextEditScreen")
        self.verticalLayout.addWidget(self.plainTextEditScreen)
        self.label_2 = QtGui.QLabel(CheckStatusDialog)
        self.label_2.setWordWrap(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.buttonBox = QtGui.QDialogButtonBox(CheckStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CheckStatusDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CheckStatusDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CheckStatusDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CheckStatusDialog)

    def retranslateUi(self, CheckStatusDialog):
        CheckStatusDialog.setWindowTitle(QtGui.QApplication.translate("CheckStatusDialog", "Checking Application Status", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CheckStatusDialog", "Checking Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCheckTitle.setText(QtGui.QApplication.translate("CheckStatusDialog", "placeholder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CheckStatusDialog", "Use the \'Options\' dialog accessible from the \'View\' menu to resolve problems shown here.  Some MAP Client features will not be available if errors have been reported.", None, QtGui.QApplication.UnicodeUTF8))

