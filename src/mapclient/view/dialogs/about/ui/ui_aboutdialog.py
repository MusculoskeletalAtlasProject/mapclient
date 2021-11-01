# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.setWindowModality(Qt.ApplicationModal)
        AboutDialog.resize(803, 644)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(AboutDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel { background-color : white }")
        self.label_2.setPixmap(QPixmap(u":/mapclient/images/logo.png"))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.aboutTextLabel = QLabel(self.frame)
        self.aboutTextLabel.setObjectName(u"aboutTextLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.aboutTextLabel.sizePolicy().hasHeightForWidth())
        self.aboutTextLabel.setSizePolicy(sizePolicy1)
        self.aboutTextLabel.setStyleSheet(u"QLabel { background-color : white; color: black }")
        self.aboutTextLabel.setTextFormat(Qt.RichText)
        self.aboutTextLabel.setWordWrap(True)
        self.aboutTextLabel.setMargin(15)

        self.verticalLayout.addWidget(self.aboutTextLabel)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_3 = QFrame(AboutDialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_Credits = QPushButton(self.frame_3)
        self.btn_Credits.setObjectName(u"btn_Credits")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_Credits.sizePolicy().hasHeightForWidth())
        self.btn_Credits.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.btn_Credits)

        self.btn_License = QPushButton(self.frame_3)
        self.btn_License.setObjectName(u"btn_License")

        self.horizontalLayout_2.addWidget(self.btn_License)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_Close = QPushButton(self.frame_3)
        self.btn_Close.setObjectName(u"btn_Close")

        self.horizontalLayout_2.addWidget(self.btn_Close)


        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)


        self.retranslateUi(AboutDialog)
        self.btn_Close.clicked.connect(AboutDialog.close)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About MAP Client", None))
        self.label_2.setText("")
        self.aboutTextLabel.setText(QCoreApplication.translate("AboutDialog", u"<p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">MAP Client ##version##</span></p><p align=\"center\">MAP Client, a program to generate detailed musculoskeletal models for OpenSim.</p><p align=\"center\">Copyright (C) 2012 University of Auckland</p><p align=\"justify\">MAP Client is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p><p align=\"justify\">MAP Client is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</p><p align=\"justify\">You should have received a copy of the GNU General Public License along with MAP Client. If not, see &lt;http://www.gnu.org/licenses/&gt;.</p><p><br/></p>", None))
        self.btn_Credits.setText(QCoreApplication.translate("AboutDialog", u"C&redits", None))
        self.btn_License.setText(QCoreApplication.translate("AboutDialog", u"&License", None))
        self.btn_Close.setText(QCoreApplication.translate("AboutDialog", u"&Close", None))
    # retranslateUi

