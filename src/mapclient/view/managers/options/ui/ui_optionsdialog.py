# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optionsdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        if not OptionsDialog.objectName():
            OptionsDialog.setObjectName(u"OptionsDialog")
        OptionsDialog.resize(581, 637)
        self.gridLayout = QGridLayout(OptionsDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(OptionsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabGeneral = QWidget()
        self.tabGeneral.setObjectName(u"tabGeneral")
        self.verticalLayout_4 = QVBoxLayout(self.tabGeneral)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.tabGeneral)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.checkBoxCheckToolsOnStartup = QCheckBox(self.groupBox)
        self.checkBoxCheckToolsOnStartup.setObjectName(u"checkBoxCheckToolsOnStartup")
        self.checkBoxCheckToolsOnStartup.setChecked(True)

        self.verticalLayout_6.addWidget(self.checkBoxCheckToolsOnStartup)

        self.checkBoxShowStepNames = QCheckBox(self.groupBox)
        self.checkBoxShowStepNames.setObjectName(u"checkBoxShowStepNames")
        self.checkBoxShowStepNames.setChecked(True)

        self.verticalLayout_6.addWidget(self.checkBoxShowStepNames)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBoxInternalWorkflowDirectory = QGroupBox(self.tabGeneral)
        self.groupBoxInternalWorkflowDirectory.setObjectName(u"groupBoxInternalWorkflowDirectory")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBoxInternalWorkflowDirectory)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEditInternalWorkflowDirectory = QLineEdit(self.groupBoxInternalWorkflowDirectory)
        self.lineEditInternalWorkflowDirectory.setObjectName(u"lineEditInternalWorkflowDirectory")

        self.horizontalLayout_4.addWidget(self.lineEditInternalWorkflowDirectory)

        self.pushButtonInternalWorkflowDirectory = QPushButton(self.groupBoxInternalWorkflowDirectory)
        self.pushButtonInternalWorkflowDirectory.setObjectName(u"pushButtonInternalWorkflowDirectory")

        self.horizontalLayout_4.addWidget(self.pushButtonInternalWorkflowDirectory)


        self.verticalLayout_4.addWidget(self.groupBoxInternalWorkflowDirectory)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tabGeneral, "")
        self.tabToolSettings = QWidget()
        self.tabToolSettings.setObjectName(u"tabToolSettings")
        self.verticalLayout_2 = QVBoxLayout(self.tabToolSettings)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxStepWizard = QGroupBox(self.tabToolSettings)
        self.groupBoxStepWizard.setObjectName(u"groupBoxStepWizard")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxStepWizard)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBoxUseExternalPySideRCC = QCheckBox(self.groupBoxStepWizard)
        self.checkBoxUseExternalPySideRCC.setObjectName(u"checkBoxUseExternalPySideRCC")

        self.verticalLayout_3.addWidget(self.checkBoxUseExternalPySideRCC)

        self.checkBoxUseExternalPySideUIC = QCheckBox(self.groupBoxStepWizard)
        self.checkBoxUseExternalPySideUIC.setObjectName(u"checkBoxUseExternalPySideUIC")

        self.verticalLayout_3.addWidget(self.checkBoxUseExternalPySideUIC)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelPySideRCC = QLabel(self.groupBoxStepWizard)
        self.labelPySideRCC.setObjectName(u"labelPySideRCC")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPySideRCC)

        self.horizontalLayoutPySideRCC = QHBoxLayout()
        self.horizontalLayoutPySideRCC.setObjectName(u"horizontalLayoutPySideRCC")
        self.lineEditPySideRCC = QLineEdit(self.groupBoxStepWizard)
        self.lineEditPySideRCC.setObjectName(u"lineEditPySideRCC")

        self.horizontalLayoutPySideRCC.addWidget(self.lineEditPySideRCC)

        self.pushButtonPySideRCC = QPushButton(self.groupBoxStepWizard)
        self.pushButtonPySideRCC.setObjectName(u"pushButtonPySideRCC")

        self.horizontalLayoutPySideRCC.addWidget(self.pushButtonPySideRCC)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayoutPySideRCC)

        self.labelPySideUIC = QLabel(self.groupBoxStepWizard)
        self.labelPySideUIC.setObjectName(u"labelPySideUIC")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPySideUIC)

        self.horizontalLayoutPySideUIC = QHBoxLayout()
        self.horizontalLayoutPySideUIC.setObjectName(u"horizontalLayoutPySideUIC")
        self.lineEditPySideUIC = QLineEdit(self.groupBoxStepWizard)
        self.lineEditPySideUIC.setObjectName(u"lineEditPySideUIC")

        self.horizontalLayoutPySideUIC.addWidget(self.lineEditPySideUIC)

        self.pushButtonPySideUIC = QPushButton(self.groupBoxStepWizard)
        self.pushButtonPySideUIC.setObjectName(u"pushButtonPySideUIC")

        self.horizontalLayoutPySideUIC.addWidget(self.pushButtonPySideUIC)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayoutPySideUIC)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.groupBoxStepWizard)

        self.groupBoxPMR = QGroupBox(self.tabToolSettings)
        self.groupBoxPMR.setObjectName(u"groupBoxPMR")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxPMR)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBoxUseExternalGit = QCheckBox(self.groupBoxPMR)
        self.checkBoxUseExternalGit.setObjectName(u"checkBoxUseExternalGit")

        self.verticalLayout_5.addWidget(self.checkBoxUseExternalGit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelGitExecutable = QLabel(self.groupBoxPMR)
        self.labelGitExecutable.setObjectName(u"labelGitExecutable")

        self.horizontalLayout_3.addWidget(self.labelGitExecutable)

        self.lineEditGitExecutable = QLineEdit(self.groupBoxPMR)
        self.lineEditGitExecutable.setObjectName(u"lineEditGitExecutable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditGitExecutable.sizePolicy().hasHeightForWidth())
        self.lineEditGitExecutable.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lineEditGitExecutable)

        self.pushButtonGitExecutable = QPushButton(self.groupBoxPMR)
        self.pushButtonGitExecutable.setObjectName(u"pushButtonGitExecutable")

        self.horizontalLayout_3.addWidget(self.pushButtonGitExecutable)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBoxPMR)

        self.groupBoxOutput = QGroupBox(self.tabToolSettings)
        self.groupBoxOutput.setObjectName(u"groupBoxOutput")
        self.verticalLayout = QVBoxLayout(self.groupBoxOutput)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plainTextEditToolTestOutput = QPlainTextEdit(self.groupBoxOutput)
        self.plainTextEditToolTestOutput.setObjectName(u"plainTextEditToolTestOutput")

        self.verticalLayout.addWidget(self.plainTextEditToolTestOutput)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonRunChecks = QPushButton(self.groupBoxOutput)
        self.pushButtonRunChecks.setObjectName(u"pushButtonRunChecks")

        self.horizontalLayout.addWidget(self.pushButtonRunChecks)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.groupBoxOutput)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tabToolSettings, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(OptionsDialog)
        self.buttonBox.accepted.connect(OptionsDialog.accept)
        self.buttonBox.rejected.connect(OptionsDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(OptionsDialog)
    # setupUi

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(QCoreApplication.translate("OptionsDialog", u"Options", None))
        self.groupBox.setTitle("")
        self.checkBoxCheckToolsOnStartup.setText(QCoreApplication.translate("OptionsDialog", u"Check tools on application start", None))
        self.checkBoxShowStepNames.setText(QCoreApplication.translate("OptionsDialog", u"Show step names", None))
        self.groupBoxInternalWorkflowDirectory.setTitle(QCoreApplication.translate("OptionsDialog", u"Internal workflow directory", None))
#if QT_CONFIG(tooltip)
        self.pushButtonInternalWorkflowDirectory.setToolTip(QCoreApplication.translate("OptionsDialog", u"Select the internal workflow directory.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonInternalWorkflowDirectory.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), QCoreApplication.translate("OptionsDialog", u"&General", None))
        self.groupBoxStepWizard.setTitle(QCoreApplication.translate("OptionsDialog", u"Step Wizard", None))
        self.checkBoxUseExternalPySideRCC.setText(QCoreApplication.translate("OptionsDialog", u"Use external PySide resource compiler (rcc)", None))
        self.checkBoxUseExternalPySideUIC.setText(QCoreApplication.translate("OptionsDialog", u"Use external PySide user interface compiler (uic)", None))
        self.labelPySideRCC.setText(QCoreApplication.translate("OptionsDialog", u"PySide rcc:", None))
#if QT_CONFIG(tooltip)
        self.lineEditPySideRCC.setToolTip(QCoreApplication.translate("OptionsDialog", u"The PySide Resource Compiler executable.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonPySideRCC.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.labelPySideUIC.setText(QCoreApplication.translate("OptionsDialog", u"PySide uic:", None))
        self.pushButtonPySideUIC.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.groupBoxPMR.setTitle(QCoreApplication.translate("OptionsDialog", u"PMR", None))
        self.checkBoxUseExternalGit.setText(QCoreApplication.translate("OptionsDialog", u"Use external Git", None))
        self.labelGitExecutable.setText(QCoreApplication.translate("OptionsDialog", u"Git:", None))
#if QT_CONFIG(tooltip)
        self.lineEditGitExecutable.setToolTip(QCoreApplication.translate("OptionsDialog", u"The Git version control executable", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonGitExecutable.setText(QCoreApplication.translate("OptionsDialog", u"...", None))
        self.groupBoxOutput.setTitle(QCoreApplication.translate("OptionsDialog", u"Tool test output", None))
        self.pushButtonRunChecks.setText(QCoreApplication.translate("OptionsDialog", u"Run Checks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabToolSettings), QCoreApplication.translate("OptionsDialog", u"Tool Settings", None))
    # retranslateUi

