# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pluginerrors.ui'
#
# Created: Thu Jan 22 14:45:54 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PluginErrors(object):
    def setupUi(self, PluginErrors):
        PluginErrors.setObjectName("PluginErrors")
        PluginErrors.resize(351, 319)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PluginErrors.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(PluginErrors)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(PluginErrors)
        self.label.setText("")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(PluginErrors)
        self.listWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideCheckBox = QtGui.QCheckBox(PluginErrors)
        self.hideCheckBox.setObjectName("hideCheckBox")
        self.horizontalLayout.addWidget(self.hideCheckBox)
        spacerItem = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ignoreButton = QtGui.QPushButton(PluginErrors)
        self.ignoreButton.setObjectName("ignoreButton")
        self.horizontalLayout.addWidget(self.ignoreButton)
        self.pushButton = QtGui.QPushButton(PluginErrors)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PluginErrors)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), PluginErrors.close)
        QtCore.QMetaObject.connectSlotsByName(PluginErrors)

    def retranslateUi(self, PluginErrors):
        PluginErrors.setWindowTitle(QtGui.QApplication.translate("PluginErrors", "Plugin Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.hideCheckBox.setText(QtGui.QApplication.translate("PluginErrors", "Don\'t show me this again", None, QtGui.QApplication.UnicodeUTF8))
        self.ignoreButton.setText(QtGui.QApplication.translate("PluginErrors", "Ignore", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("PluginErrors", "OK", None, QtGui.QApplication.UnicodeUTF8))

