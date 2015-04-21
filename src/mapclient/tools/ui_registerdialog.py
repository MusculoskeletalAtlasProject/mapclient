# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/registerdialog.ui'
#
# Created: Tue Jun 18 10:10:05 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        RegisterDialog.setObjectName("RegisterDialog")
        RegisterDialog.resize(447, 263)
        self.verticalLayout = QtGui.QVBoxLayout(RegisterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(RegisterDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.usernameLineEdit = QtGui.QLineEdit(self.groupBox)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.usernameLineEdit)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.passwordLineEdit = QtGui.QLineEdit(self.groupBox)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.confirmPasswordLineEdit = QtGui.QLineEdit(self.groupBox)
        self.confirmPasswordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.confirmPasswordLineEdit.setObjectName("confirmPasswordLineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.confirmPasswordLineEdit)
        self.emailLineEdit = QtGui.QLineEdit(self.groupBox)
        self.emailLineEdit.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.emailLineEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(RegisterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RegisterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), RegisterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), RegisterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegisterDialog)
        RegisterDialog.setTabOrder(self.usernameLineEdit, self.emailLineEdit)
        RegisterDialog.setTabOrder(self.emailLineEdit, self.passwordLineEdit)
        RegisterDialog.setTabOrder(self.passwordLineEdit, self.confirmPasswordLineEdit)
        RegisterDialog.setTabOrder(self.confirmPasswordLineEdit, self.buttonBox)

    def retranslateUi(self, RegisterDialog):
        RegisterDialog.setWindowTitle(QtGui.QApplication.translate("RegisterDialog", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("RegisterDialog", "Register:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RegisterDialog", "Username: *", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("RegisterDialog", "E-mail: *", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RegisterDialog", "Password: *", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RegisterDialog", "Confirm password: *", None, QtGui.QApplication.UnicodeUTF8))

