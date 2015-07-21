# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pmrworkflowwidget.ui'
#
# Created: Mon Jul 20 17:08:13 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PMRWorkflowWidget(object):
    def setupUi(self, PMRWorkflowWidget):
        PMRWorkflowWidget.setObjectName("PMRWorkflowWidget")
        PMRWorkflowWidget.resize(791, 711)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PMRWorkflowWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.labelLink = QtGui.QLabel(PMRWorkflowWidget)
        self.labelLink.setObjectName("labelLink")
        self.gridLayout.addWidget(self.labelLink, 0, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(PMRWorkflowWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBoxSearch = QtGui.QComboBox(self.groupBox)
        self.comboBoxSearch.setObjectName("comboBoxSearch")
        self.comboBoxSearch.addItem("")
        self.comboBoxSearch.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBoxSearch)
        self.lineEditSearch = QtGui.QLineEdit(self.groupBox)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.horizontalLayout_2.addWidget(self.lineEditSearch)
        self.pushButtonSearch = QtGui.QPushButton(self.groupBox)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.horizontalLayout_2.addWidget(self.pushButtonSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidgetResults = QtGui.QListWidget(self.groupBox)
        self.listWidgetResults.setObjectName("listWidgetResults")
        self.verticalLayout.addWidget(self.listWidgetResults)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditWorkspace = QtGui.QLineEdit(self.groupBox)
        self.lineEditWorkspace.setObjectName("lineEditWorkspace")
        self.horizontalLayout.addWidget(self.lineEditWorkspace)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonImport = QtGui.QPushButton(PMRWorkflowWidget)
        self.pushButtonImport.setObjectName("pushButtonImport")
        self.horizontalLayout_3.addWidget(self.pushButtonImport)
        self.pushButtonExport = QtGui.QPushButton(PMRWorkflowWidget)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.horizontalLayout_3.addWidget(self.pushButtonExport)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label.setBuddy(self.lineEditWorkspace)

        self.retranslateUi(PMRWorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(PMRWorkflowWidget)

    def retranslateUi(self, PMRWorkflowWidget):
        PMRWorkflowWidget.setWindowTitle(QtGui.QApplication.translate("PMRWorkflowWidget", "PMR Workflow Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLink.setText(QtGui.QApplication.translate("PMRWorkflowWidget", "<a href=\"mapclient.register\">register</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PMRWorkflowWidget", "Physiome Model Repository", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSearch.setItemText(0, QtGui.QApplication.translate("PMRWorkflowWidget", "Ontological term", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxSearch.setItemText(1, QtGui.QApplication.translate("PMRWorkflowWidget", "Plain text", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSearch.setText(QtGui.QApplication.translate("PMRWorkflowWidget", "&Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PMRWorkflowWidget", "Workspace:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonImport.setToolTip(QtGui.QApplication.translate("PMRWorkflowWidget", "Import to local location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonImport.setText(QtGui.QApplication.translate("PMRWorkflowWidget", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonExport.setToolTip(QtGui.QApplication.translate("PMRWorkflowWidget", "Export from local location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonExport.setText(QtGui.QApplication.translate("PMRWorkflowWidget", "Export", None, QtGui.QApplication.UnicodeUTF8))

