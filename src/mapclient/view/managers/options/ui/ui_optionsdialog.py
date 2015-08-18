# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/optionsdialog.ui'
#
# Created: Mon Jun 29 14:45:27 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.resize(525, 556)
        self.gridLayout = QtGui.QGridLayout(OptionsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.gridLayout_3 = QtGui.QGridLayout(self.tabGeneral)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 1, 1, 1)
        self.checkBoxShowStepNames = QtGui.QCheckBox(self.tabGeneral)
        self.checkBoxShowStepNames.setChecked(True)
        self.checkBoxShowStepNames.setObjectName("checkBoxShowStepNames")
        self.gridLayout_3.addWidget(self.checkBoxShowStepNames, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabGeneral, "")
        self.tabToolSettings = QtGui.QWidget()
        self.tabToolSettings.setObjectName("tabToolSettings")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabToolSettings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtGui.QGroupBox(self.tabToolSettings)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName("formLayout")
        self.labelVirtualEnvironmentPath = QtGui.QLabel(self.groupBox_3)
        self.labelVirtualEnvironmentPath.setObjectName("labelVirtualEnvironmentPath")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelVirtualEnvironmentPath)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditVirtualEnvironmentPath = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditVirtualEnvironmentPath.sizePolicy().hasHeightForWidth())
        self.lineEditVirtualEnvironmentPath.setSizePolicy(sizePolicy)
        self.lineEditVirtualEnvironmentPath.setObjectName("lineEditVirtualEnvironmentPath")
        self.horizontalLayout_2.addWidget(self.lineEditVirtualEnvironmentPath)
        self.pushButtonVirtualEnvironmentPath = QtGui.QPushButton(self.groupBox_3)
        self.pushButtonVirtualEnvironmentPath.setObjectName("pushButtonVirtualEnvironmentPath")
        self.horizontalLayout_2.addWidget(self.pushButtonVirtualEnvironmentPath)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.checkBoxDontCreateVirtualEnvironment = QtGui.QCheckBox(self.groupBox_3)
        self.checkBoxDontCreateVirtualEnvironment.setEnabled(False)
        self.checkBoxDontCreateVirtualEnvironment.setObjectName("checkBoxDontCreateVirtualEnvironment")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBoxDontCreateVirtualEnvironment)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.tabToolSettings)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditPySideUIC = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditPySideUIC.setObjectName("lineEditPySideUIC")
        self.gridLayout_2.addWidget(self.lineEditPySideUIC, 0, 1, 1, 1)
        self.pushButtonPySideUIC = QtGui.QPushButton(self.groupBox_4)
        self.pushButtonPySideUIC.setObjectName("pushButtonPySideUIC")
        self.gridLayout_2.addWidget(self.pushButtonPySideUIC, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditPySideRCC = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditPySideRCC.setObjectName("lineEditPySideRCC")
        self.gridLayout_2.addWidget(self.lineEditPySideRCC, 1, 1, 1, 1)
        self.pushButtonPySideRCC = QtGui.QPushButton(self.groupBox_4)
        self.pushButtonPySideRCC.setObjectName("pushButtonPySideRCC")
        self.gridLayout_2.addWidget(self.pushButtonPySideRCC, 1, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QtGui.QGroupBox(self.tabToolSettings)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelGitExecutable = QtGui.QLabel(self.groupBox_5)
        self.labelGitExecutable.setObjectName("labelGitExecutable")
        self.horizontalLayout_3.addWidget(self.labelGitExecutable)
        self.lineEditGitExecutable = QtGui.QLineEdit(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditGitExecutable.sizePolicy().hasHeightForWidth())
        self.lineEditGitExecutable.setSizePolicy(sizePolicy)
        self.lineEditGitExecutable.setObjectName("lineEditGitExecutable")
        self.horizontalLayout_3.addWidget(self.lineEditGitExecutable)
        self.pushButtonGitExecutable = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonGitExecutable.setObjectName("pushButtonGitExecutable")
        self.horizontalLayout_3.addWidget(self.pushButtonGitExecutable)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox = QtGui.QGroupBox(self.tabToolSettings)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEditToolTestOutput = QtGui.QPlainTextEdit(self.groupBox)
        self.plainTextEditToolTestOutput.setObjectName("plainTextEditToolTestOutput")
        self.verticalLayout.addWidget(self.plainTextEditToolTestOutput)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonRunChecks = QtGui.QPushButton(self.groupBox)
        self.pushButtonRunChecks.setObjectName("pushButtonRunChecks")
        self.horizontalLayout.addWidget(self.pushButtonRunChecks)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabWidget.addTab(self.tabToolSettings, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(OptionsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), OptionsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(QtGui.QApplication.translate("OptionsDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStepNames.setText(QtGui.QApplication.translate("OptionsDialog", "Show step names", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), QtGui.QApplication.translate("OptionsDialog", "&General", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("OptionsDialog", "Virtual Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVirtualEnvironmentPath.setText(QtGui.QApplication.translate("OptionsDialog", "Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditVirtualEnvironmentPath.setToolTip(QtGui.QApplication.translate("OptionsDialog", "The virtual environment path has some restrictions, for instance it cannot have any spaces in it.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVirtualEnvironmentPath.setText(QtGui.QApplication.translate("OptionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDontCreateVirtualEnvironment.setText(QtGui.QApplication.translate("OptionsDialog", "Don\'t create a virtual environment", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("OptionsDialog", "Step Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OptionsDialog", "pyside-uic:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPySideUIC.setToolTip(QtGui.QApplication.translate("OptionsDialog", "The PySide User Interface Compiler executable", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPySideUIC.setText(QtGui.QApplication.translate("OptionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("OptionsDialog", "pyside-rcc", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPySideRCC.setToolTip(QtGui.QApplication.translate("OptionsDialog", "The PySide Resource Compiler executable.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPySideRCC.setText(QtGui.QApplication.translate("OptionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("OptionsDialog", "PMR", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGitExecutable.setText(QtGui.QApplication.translate("OptionsDialog", "Git:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditGitExecutable.setToolTip(QtGui.QApplication.translate("OptionsDialog", "The Git version control executable", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGitExecutable.setText(QtGui.QApplication.translate("OptionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("OptionsDialog", "Tool test output", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRunChecks.setText(QtGui.QApplication.translate("OptionsDialog", "Run Checks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabToolSettings), QtGui.QApplication.translate("OptionsDialog", "Tool Settings", None, QtGui.QApplication.UnicodeUTF8))
