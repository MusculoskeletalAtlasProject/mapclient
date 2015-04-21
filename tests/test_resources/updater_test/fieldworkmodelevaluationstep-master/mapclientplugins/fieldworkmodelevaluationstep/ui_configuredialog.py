# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuredialog.ui'
#
# Created: Mon Jan 13 15:41:17 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(418, 303)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.configGroupBox = QtGui.QGroupBox(Dialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtGui.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label0)
        self.lineEdit0 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName("lineEdit0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit0)
        self.label1 = QtGui.QLabel(self.configGroupBox)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineEdit1 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit1.setObjectName("lineEdit1")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit1)
        self.label2 = QtGui.QLabel(self.configGroupBox)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label2)
        self.lineEdit2 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit2.setObjectName("lineEdit2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit2)
        self.lineEdit3 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit3.setObjectName("lineEdit3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit3)
        self.label3 = QtGui.QLabel(self.configGroupBox)
        self.label3.setObjectName("label3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label3)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ConfigureDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label0.setText(QtGui.QApplication.translate("Dialog", "identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("Dialog", "discretisation:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "node coordinates:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Dialog", "elements:", None, QtGui.QApplication.UnicodeUTF8))

