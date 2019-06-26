# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/tools/pmr/qt/pmrworkflowwidget.ui',
# licensing of 'src/mapclient/tools/pmr/qt/pmrworkflowwidget.ui' applies.
#
# Created: Wed Jun 26 11:28:03 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PMRWorkflowWidget(object):
    def setupUi(self, PMRWorkflowWidget):
        PMRWorkflowWidget.setObjectName("PMRWorkflowWidget")
        PMRWorkflowWidget.resize(791, 711)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PMRWorkflowWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.labelLink = QtWidgets.QLabel(PMRWorkflowWidget)
        self.labelLink.setObjectName("labelLink")
        self.gridLayout.addWidget(self.labelLink, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(PMRWorkflowWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBoxSearch = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxSearch.setObjectName("comboBoxSearch")
        self.comboBoxSearch.addItem("")
        self.comboBoxSearch.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBoxSearch)
        self.lineEditSearch = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.horizontalLayout_2.addWidget(self.lineEditSearch)
        self.pushButtonSearch = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.horizontalLayout_2.addWidget(self.pushButtonSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidgetResults = QtWidgets.QListWidget(self.groupBox)
        self.listWidgetResults.setObjectName("listWidgetResults")
        self.verticalLayout.addWidget(self.listWidgetResults)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditWorkspace = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditWorkspace.setObjectName("lineEditWorkspace")
        self.horizontalLayout.addWidget(self.lineEditWorkspace)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonImport = QtWidgets.QPushButton(PMRWorkflowWidget)
        self.pushButtonImport.setObjectName("pushButtonImport")
        self.horizontalLayout_3.addWidget(self.pushButtonImport)
        self.pushButtonExport = QtWidgets.QPushButton(PMRWorkflowWidget)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.horizontalLayout_3.addWidget(self.pushButtonExport)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label.setBuddy(self.lineEditWorkspace)

        self.retranslateUi(PMRWorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(PMRWorkflowWidget)

    def retranslateUi(self, PMRWorkflowWidget):
        PMRWorkflowWidget.setWindowTitle(QtWidgets.QApplication.translate("PMRWorkflowWidget", "PMR Workflow Tool", None, -1))
        self.labelLink.setText(QtWidgets.QApplication.translate("PMRWorkflowWidget", "<a href=\"mapclient.register\">register</a>", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Physiome Model Repository", None, -1))
        self.comboBoxSearch.setItemText(0, QtWidgets.QApplication.translate("PMRWorkflowWidget", "Ontological term", None, -1))
        self.comboBoxSearch.setItemText(1, QtWidgets.QApplication.translate("PMRWorkflowWidget", "Plain text", None, -1))
        self.pushButtonSearch.setText(QtWidgets.QApplication.translate("PMRWorkflowWidget", "&Search", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Workspace:", None, -1))
        self.pushButtonImport.setToolTip(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Import to local location", None, -1))
        self.pushButtonImport.setText(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Import", None, -1))
        self.pushButtonExport.setToolTip(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Export from local location", None, -1))
        self.pushButtonExport.setText(QtWidgets.QApplication.translate("PMRWorkflowWidget", "Export", None, -1))

