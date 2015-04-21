# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pmrdvcscommitdialog.ui'
#
# Created: Tue Apr  7 20:43:05 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PMRDVCSCommitDialog(object):
    def setupUi(self, PMRDVCSCommitDialog):
        PMRDVCSCommitDialog.setObjectName("PMRDVCSCommitDialog")
        PMRDVCSCommitDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PMRDVCSCommitDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(PMRDVCSCommitDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.commentTextEdit = QtGui.QPlainTextEdit(self.groupBox)
        self.commentTextEdit.setObjectName("commentTextEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.commentTextEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(PMRDVCSCommitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.SaveAll)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.commentTextEdit)

        self.retranslateUi(PMRDVCSCommitDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PMRDVCSCommitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PMRDVCSCommitDialog)
        PMRDVCSCommitDialog.setTabOrder(self.commentTextEdit, self.buttonBox)

    def retranslateUi(self, PMRDVCSCommitDialog):
        PMRDVCSCommitDialog.setWindowTitle(QtGui.QApplication.translate("PMRDVCSCommitDialog", "PMR Workspace Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PMRDVCSCommitDialog", "PMR Workspace Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PMRDVCSCommitDialog", "commen&t:", None, QtGui.QApplication.UnicodeUTF8))
        self.commentTextEdit.setPlainText(QtGui.QApplication.translate("PMRDVCSCommitDialog", "Lazy commit message from MAP Client.", None, QtGui.QApplication.UnicodeUTF8))

