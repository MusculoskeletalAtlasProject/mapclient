"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QTabWidget, QWidget, QVBoxLayout, QLabel

from mapclient.view.dialogs.about.ui.ui_creditsdialog import Ui_CreditsDialog
from mapclient.settings import info


class CreditsDialog(QDialog):
    """
    Dialog to display the credits.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_CreditsDialog()
        self._ui.setupUi(self)

        creditsTab = QTabWidget()
        creditSections = list(info.CREDITS.keys())
        for creditSection in creditSections:
            creditTab = QWidget()
            creditsTab.addTab(creditTab, creditSection)
            vbox = QVBoxLayout(creditTab)
            creditList = ""
            for person in info.CREDITS[creditSection]:
                creditList += ("\n%s [%s]" % (person['name'], person['email']))
            creditLabel = QLabel()
            creditLabel.setMargin(15)
            creditLabel.setStyleSheet("QLabel { background-color : white; color: black}")
            creditLabel.setText(creditList)
            creditLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            vbox.addWidget(creditLabel)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(creditsTab)
        self._ui.frame_CreditsTab.setLayout(vbox)

