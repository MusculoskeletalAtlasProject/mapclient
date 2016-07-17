# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/aboutdialog.ui'
#
# Created: Thu Jul 10 13:20:15 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AboutDialog.resize(518, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(AboutDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtGui.QFrame(AboutDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/mapclient/images/logo.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.aboutTextLabel = QtGui.QLabel(self.frame)
        self.aboutTextLabel.setStyleSheet("QLabel { background-color : white }")
        self.aboutTextLabel.setWordWrap(True)
        self.aboutTextLabel.setObjectName("aboutTextLabel")
        self.verticalLayout.addWidget(self.aboutTextLabel)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(AboutDialog)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_Credits = QtGui.QPushButton(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Credits.sizePolicy().hasHeightForWidth())
        self.btn_Credits.setSizePolicy(sizePolicy)
        self.btn_Credits.setObjectName("btn_Credits")
        self.horizontalLayout_2.addWidget(self.btn_Credits)
        self.btn_License = QtGui.QPushButton(self.frame_3)
        self.btn_License.setObjectName("btn_License")
        self.horizontalLayout_2.addWidget(self.btn_License)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_Close = QtGui.QPushButton(self.frame_3)
        self.btn_Close.setObjectName("btn_Close")
        self.horizontalLayout_2.addWidget(self.btn_Close)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.btn_Close, QtCore.SIGNAL("clicked()"), AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About MAP Client", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutTextLabel.setText(QtGui.QApplication.translate("AboutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">MAP Client ##version##</span></p><p align=\"center\">MAP Client, a program to generate detailed musculoskeletal models for OpenSim.</p><p align=\"center\">Copyright (C) 2012 University of Auckland</p><p align=\"justify\">MAP Client is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p><p align=\"justify\">MAP Client is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</p><p align=\"justify\">You should have received a copy of the GNU General Public License along with MAP Client. If not, see &lt;http://www.gnu.org/licenses/&gt;.</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Credits.setText(QtGui.QApplication.translate("AboutDialog", "C&redits", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_License.setText(QtGui.QApplication.translate("AboutDialog", "&License", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Close.setText(QtGui.QApplication.translate("AboutDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))
