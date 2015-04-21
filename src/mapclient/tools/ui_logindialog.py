# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/logindialog.ui'
#
# Created: Tue Jun 18 14:53:09 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(394, 283)
        self.verticalLayout = QtGui.QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(LoginDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.usernameLineEdit = QtGui.QLineEdit(self.groupBox)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.usernameLineEdit)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.passwordLineEdit = QtGui.QLineEdit(self.groupBox)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.rememberMeCheckBox = QtGui.QCheckBox(self.groupBox)
        self.rememberMeCheckBox.setObjectName("rememberMeCheckBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.rememberMeCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtGui.QFormLayout.FieldRole, spacerItem)
        self.registerForgotLabel = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.registerForgotLabel.setFont(font)
        self.registerForgotLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.registerForgotLabel.setObjectName("registerForgotLabel")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.registerForgotLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtGui.QFormLayout.FieldRole, spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.errorOutputLabel = QtGui.QLabel(self.groupBox)
        self.errorOutputLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.errorOutputLabel.setObjectName("errorOutputLabel")
        self.horizontalLayout.addWidget(self.errorOutputLabel)
        self.formLayout.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(LoginDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LoginDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)
        LoginDialog.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        LoginDialog.setTabOrder(self.passwordLineEdit, self.rememberMeCheckBox)
        LoginDialog.setTabOrder(self.rememberMeCheckBox, self.buttonBox)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QtGui.QApplication.translate("LoginDialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LoginDialog", "Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginDialog", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginDialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.rememberMeCheckBox.setText(QtGui.QApplication.translate("LoginDialog", "Remember me", None, QtGui.QApplication.UnicodeUTF8))
        self.registerForgotLabel.setText(QtGui.QApplication.translate("LoginDialog", "<html><head/><body><p>Need to <a href=\"mapclient.register\"><span style=\" text-decoration: underline; color:#0000ff;\">register</span></a>? or <a href=\"mapclient.forgot\"><span style=\" text-decoration: underline; color:#0000ff;\">forgot</span></a> password?</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.errorOutputLabel.setText(QtGui.QApplication.translate("LoginDialog", "   ", None, QtGui.QApplication.UnicodeUTF8))

