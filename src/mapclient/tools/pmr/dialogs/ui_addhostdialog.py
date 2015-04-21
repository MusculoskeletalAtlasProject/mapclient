# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/addhostdialog.ui'
#
# Created: Mon Mar  2 14:17:30 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AddHostDialog(object):
    def setupUi(self, AddHostDialog):
        AddHostDialog.setObjectName("AddHostDialog")
        AddHostDialog.resize(360, 104)
        self.verticalLayout = QtGui.QVBoxLayout(AddHostDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(AddHostDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.urlLineEdit = QtGui.QLineEdit(self.groupBox)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.horizontalLayout.addWidget(self.urlLineEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(AddHostDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddHostDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddHostDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddHostDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddHostDialog)

    def retranslateUi(self, AddHostDialog):
        AddHostDialog.setWindowTitle(QtGui.QApplication.translate("AddHostDialog", "Add Host", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("AddHostDialog", "PMR Web Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddHostDialog", "url: ", None, QtGui.QApplication.UnicodeUTF8))

