# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/oauthcheckdialog.ui'
#
# Created: Fri Nov 22 16:57:05 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_OAuthCheckDialog(object):
    def setupUi(self, OAuthCheckDialog):
        OAuthCheckDialog.setObjectName("OAuthCheckDialog")
        OAuthCheckDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(OAuthCheckDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(OAuthCheckDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.continueButton = QtGui.QPushButton(self.groupBox)
        self.continueButton.setDefault(True)
        self.continueButton.setObjectName("continueButton")
        self.verticalLayout_2.addWidget(self.continueButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(OAuthCheckDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OAuthCheckDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), OAuthCheckDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), OAuthCheckDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OAuthCheckDialog)

    def retranslateUi(self, OAuthCheckDialog):
        OAuthCheckDialog.setWindowTitle(QtGui.QApplication.translate("OAuthCheckDialog", "Access Credentials Required", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("OAuthCheckDialog", "Authorise Application", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OAuthCheckDialog", "MAP Client requires your permission to access PMR.", None, QtGui.QApplication.UnicodeUTF8))
        self.continueButton.setText(QtGui.QApplication.translate("OAuthCheckDialog", "Continue", None, QtGui.QApplication.UnicodeUTF8))

