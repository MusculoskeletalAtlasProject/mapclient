# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuredialog.ui'
#
# Created: Sat May 31 23:14:20 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(418, 391)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.configGroupBox = QtGui.QGroupBox(Dialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtGui.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label0)
        self.lineEdit0 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName("lineEdit0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit0)
        self.label_2 = QtGui.QLabel(self.configGroupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditFHC = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditFHC.setObjectName("lineEditFHC")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditFHC)
        self.label_3 = QtGui.QLabel(self.configGroupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditMEC = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditMEC.setObjectName("lineEditMEC")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditMEC)
        self.label_4 = QtGui.QLabel(self.configGroupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEditLEC = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditLEC.setObjectName("lineEditLEC")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEditLEC)
        self.label_5 = QtGui.QLabel(self.configGroupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEditFGT = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditFGT.setObjectName("lineEditFGT")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEditFGT)
        self.label_7 = QtGui.QLabel(self.configGroupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_7)
        self.checkBoxGUI = QtGui.QCheckBox(self.configGroupBox)
        self.checkBoxGUI.setText("")
        self.checkBoxGUI.setObjectName("checkBoxGUI")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBoxGUI)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ConfigureDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label0.setText(QtGui.QApplication.translate("Dialog", "identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Femoral Head Centre:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Medial Epicondyle:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Lateral Epicondyle:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Greater Trochanter:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "GUI:", None, QtGui.QApplication.UnicodeUTF8))

