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
from dateutil.parser import parse

from PySide2.QtWidgets import QDialog, QTableWidgetItem, QLabel

from mapclient.view.dialogs.log.ui.ui_loginformation import Ui_LogInformation
from mapclient.settings.general import get_log_location


class LogInformation(QDialog):
    """
    Log record dialog to present the user with the log information recorded by the program.
    """

    current_log_file = get_log_location()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_LogInformation()
        self._ui.setupUi(self)
        self._ui.detailsButton.setEnabled(False)
        self._make_connections()

    def fillTable(self, parent=None):
        logs = self.loadSession(get_log_location())
        self.updateTable(logs)

    def _make_connections(self):
        self._ui.information_table.itemSelectionChanged.connect(self._selection_changed)
        self._ui.information_table.cellDoubleClicked.connect(self.showLogDetails)
        self._ui.detailsButton.clicked.connect(self.showLogDetails)
        self._ui.loadButton.clicked.connect(self.loadLogSession)

    def _selection_changed(self):
        if self._ui.information_table.selectedItems():
            self._ui.detailsButton.setEnabled(True)

    def showLogDetails(self):
        from mapclient.view.dialogs.log.logdetails import LogDetails
        dlg = LogDetails(self)
        dlg.setModal(True)
        index = self._ui.information_table.indexFromItem(self._ui.information_table.selectedItems()[0])
        row = index.row()
        log_details = []
        for column in range(self._ui.information_table.columnCount()):
            if column == 4:
                edit = self._ui.information_table.cellWidget(row, column)
                text = edit.text()
            else:
                text = self._ui.information_table.item(row, column).text()
            log_details.append(text)
        dlg.fillTable(log_details)
        dlg.exec_()

    def loadLogSession(self):
        from mapclient.view.dialogs.log.loadlogsession import LoadLogSession
        dlg = LoadLogSession(self)
        dlg.setModal(True)
        if dlg.exec_():
            log_file = dlg.getLogSession()
            logs = self.loadSession(log_file)
            if logs:
                self.updateTable(logs)
                self.current_log_file = log_file

    def loadSession(self, filename):
        logs = []
        with open(filename, 'r') as f:
            log_data = [line.rstrip('\n') for line in f]
            for entry in log_data:
                if entry:
                    try:
                        parse(entry[:25])
                        logs.append(entry.split(' - '))
                    except Exception:
                        logs[-1][-1] += '\n' + entry

        return logs

    def updateTable(self, logs):
        self._ui.information_table.clearContents()
        self._ui.information_table.setRowCount(len(logs))
        self._ui.information_table.setColumnCount(5)
        self._ui.information_table.setColumnHidden(0, True)
        self._ui.information_table.setColumnHidden(2, True)

        for row, log in enumerate(logs):
            for column, entry in enumerate(log):
                if column == 4:
                    label = QLabel(entry)
                    self._ui.information_table.setCellWidget(row, column, label)
                else:
                    self._ui.information_table.setItem(row, column, QTableWidgetItem(entry))

        self._ui.information_table.resizeColumnToContents(0)
        self._ui.information_table.resizeColumnToContents(1)
        self._ui.information_table.resizeRowsToContents()
