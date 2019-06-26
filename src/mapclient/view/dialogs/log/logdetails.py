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
from PySide2.QtWidgets import QDialog, QTableWidgetItem, QLabel

from mapclient.view.dialogs.log.ui.ui_logdetails import Ui_LogDetails


class LogDetails(QDialog):
    """
    Load details dialog to present the user with more detailed information about an individual recorded log.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_LogDetails()
        self._ui.setupUi(self)

    def fillTable(self, log_details):
        self._ui.detailedTable.setRowCount(5)
        self._ui.detailedTable.setColumnCount(1)

        for row, information in enumerate(log_details):
            if row == 4:
                label = QLabel(information)
                self._ui.detailedTable.setCellWidget(row, 0, label)
            else:
                self._ui.detailedTable.setItem(row, 0, QTableWidgetItem(information))

        self._ui.detailedTable.resizeColumnsToContents()
        self._ui.detailedTable.resizeRowsToContents()
