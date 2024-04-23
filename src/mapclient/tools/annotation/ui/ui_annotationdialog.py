# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotationdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AnnotationDialog(object):
    def setupUi(self, AnnotationDialog):
        if not AnnotationDialog.objectName():
            AnnotationDialog.setObjectName(u"AnnotationDialog")
        AnnotationDialog.resize(462, 560)
        self.verticalLayout_2 = QVBoxLayout(AnnotationDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(AnnotationDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.locationLineEdit = QLineEdit(self.groupBox)
        self.locationLineEdit.setObjectName(u"locationLineEdit")
        self.locationLineEdit.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.locationLineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.subjectComboBox = QComboBox(self.groupBox)
        self.subjectComboBox.setObjectName(u"subjectComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectComboBox.sizePolicy().hasHeightForWidth())
        self.subjectComboBox.setSizePolicy(sizePolicy)
        self.subjectComboBox.setEditable(True)

        self.horizontalLayout.addWidget(self.subjectComboBox)

        self.predicateComboBox = QComboBox(self.groupBox)
        self.predicateComboBox.setObjectName(u"predicateComboBox")
        sizePolicy.setHeightForWidth(self.predicateComboBox.sizePolicy().hasHeightForWidth())
        self.predicateComboBox.setSizePolicy(sizePolicy)
        self.predicateComboBox.setEditable(True)

        self.horizontalLayout.addWidget(self.predicateComboBox)

        self.objectComboBox = QComboBox(self.groupBox)
        self.objectComboBox.setObjectName(u"objectComboBox")
        sizePolicy.setHeightForWidth(self.objectComboBox.sizePolicy().hasHeightForWidth())
        self.objectComboBox.setSizePolicy(sizePolicy)
        self.objectComboBox.setEditable(True)

        self.horizontalLayout.addWidget(self.objectComboBox)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.addButton = QPushButton(self.groupBox)
        self.addButton.setObjectName(u"addButton")

        self.gridLayout.addWidget(self.addButton, 1, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(0, 16777215))

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.annotationListWidget = QListWidget(self.groupBox)
        self.annotationListWidget.setObjectName(u"annotationListWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.annotationListWidget.sizePolicy().hasHeightForWidth())
        self.annotationListWidget.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.annotationListWidget, 3, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.removeButton = QPushButton(self.groupBox)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout.addWidget(self.removeButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)

        self.fileButton = QPushButton(self.groupBox)
        self.fileButton.setObjectName(u"fileButton")

        self.gridLayout.addWidget(self.fileButton, 0, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(AnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(AnnotationDialog)
        self.buttonBox.rejected.connect(AnnotationDialog.reject)

        QMetaObject.connectSlotsByName(AnnotationDialog)
    # setupUi

    def retranslateUi(self, AnnotationDialog):
        AnnotationDialog.setWindowTitle(QCoreApplication.translate("AnnotationDialog", u"Annotation Tool", None))
        self.groupBox.setTitle(QCoreApplication.translate("AnnotationDialog", u"Annotation Tool", None))
        self.label_2.setText(QCoreApplication.translate("AnnotationDialog", u"Location:", None))
        self.addButton.setText(QCoreApplication.translate("AnnotationDialog", u"Add", None))
        self.label.setText(QCoreApplication.translate("AnnotationDialog", u"Annotations:", None))
        self.label_3.setText(QCoreApplication.translate("AnnotationDialog", u"TextLabel", None))
        self.removeButton.setText(QCoreApplication.translate("AnnotationDialog", u"Remove", None))
        self.fileButton.setText(QCoreApplication.translate("AnnotationDialog", u"...", None))
    # retranslateUi

