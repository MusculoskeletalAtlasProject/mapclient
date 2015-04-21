# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/misc.ui'
#
# Created: Fri Dec 12 11:45:10 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Misc(object):
    def setupUi(self, Misc):
        Misc.setObjectName("Misc")
        Misc.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(Misc)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Misc)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.authorNameLineEdit = QtGui.QLineEdit(Misc)
        self.authorNameLineEdit.setObjectName("authorNameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.authorNameLineEdit)
        self.label_2 = QtGui.QLabel(Misc)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.categoryLineEdit = QtGui.QLineEdit(Misc)
        self.categoryLineEdit.setObjectName("categoryLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.categoryLineEdit)
        self.label_3 = QtGui.QLabel(Misc)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.pluginLocationEdit = QtGui.QLineEdit(Misc)
        self.pluginLocationEdit.setObjectName("pluginLocationEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pluginLocationEdit)
        self.label.setBuddy(self.authorNameLineEdit)
        self.label_2.setBuddy(self.categoryLineEdit)
        self.label_3.setBuddy(self.pluginLocationEdit)

        self.retranslateUi(Misc)
        QtCore.QMetaObject.connectSlotsByName(Misc)

    def retranslateUi(self, Misc):
        Misc.setWindowTitle(QtGui.QApplication.translate("Misc", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Misc", "Author name(s):  ", None, QtGui.QApplication.UnicodeUTF8))
        self.authorNameLineEdit.setPlaceholderText(QtGui.QApplication.translate("Misc", "Xxxx Yyyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Misc", "Category:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.categoryLineEdit.setPlaceholderText(QtGui.QApplication.translate("Misc", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Misc", "Plugin Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginLocationEdit.setPlaceholderText(QtGui.QApplication.translate("Misc", "eg. https://github.com.../archive/master.zip", None, QtGui.QApplication.UnicodeUTF8))

