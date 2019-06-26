# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/tools/pmr/qt/authoriseapplicationdialog.ui',
# licensing of 'src/mapclient/tools/pmr/qt/authoriseapplicationdialog.ui' applies.
#
# Created: Wed Jun 26 11:30:03 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AuthoriseApplicationDialog(object):
    def setupUi(self, AuthoriseApplicationDialog):
        AuthoriseApplicationDialog.setObjectName("AuthoriseApplicationDialog")
        AuthoriseApplicationDialog.resize(482, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(AuthoriseApplicationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(AuthoriseApplicationDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tokenLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.tokenLineEdit.setObjectName("tokenLineEdit")
        self.verticalLayout_2.addWidget(self.tokenLineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 122, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(AuthoriseApplicationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuthoriseApplicationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuthoriseApplicationDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuthoriseApplicationDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AuthoriseApplicationDialog)

    def retranslateUi(self, AuthoriseApplicationDialog):
        AuthoriseApplicationDialog.setWindowTitle(QtWidgets.QApplication.translate("AuthoriseApplicationDialog", "Authorise Application", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("AuthoriseApplicationDialog", "Authorise Application", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AuthoriseApplicationDialog", "Paste authorisation token here:", None, -1))

