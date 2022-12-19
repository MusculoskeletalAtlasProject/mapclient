# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmrdvcscommitdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PMRDVCSCommitDialog(object):
    def setupUi(self, PMRDVCSCommitDialog):
        if not PMRDVCSCommitDialog.objectName():
            PMRDVCSCommitDialog.setObjectName(u"PMRDVCSCommitDialog")
        PMRDVCSCommitDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(PMRDVCSCommitDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(PMRDVCSCommitDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.commentTextEdit = QPlainTextEdit(self.groupBox)
        self.commentTextEdit.setObjectName(u"commentTextEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.commentTextEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(PMRDVCSCommitDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Save|QDialogButtonBox.SaveAll)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label_3.setBuddy(self.commentTextEdit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.commentTextEdit, self.buttonBox)

        self.retranslateUi(PMRDVCSCommitDialog)
        self.buttonBox.rejected.connect(PMRDVCSCommitDialog.reject)

        QMetaObject.connectSlotsByName(PMRDVCSCommitDialog)
    # setupUi

    def retranslateUi(self, PMRDVCSCommitDialog):
        PMRDVCSCommitDialog.setWindowTitle(QCoreApplication.translate("PMRDVCSCommitDialog", u"PMR Workspace Commit", None))
        self.groupBox.setTitle(QCoreApplication.translate("PMRDVCSCommitDialog", u"PMR Workspace Commit", None))
        self.label_3.setText(QCoreApplication.translate("PMRDVCSCommitDialog", u"commen&t:", None))
        self.commentTextEdit.setPlainText(QCoreApplication.translate("PMRDVCSCommitDialog", u"Lazy commit message from MAP Client.", None))
    # retranslateUi

