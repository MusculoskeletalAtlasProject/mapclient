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
from PySide6.QtWidgets import QDialog, QTableWidgetItem

from mapclient.view.dialogs.about.ui.ui_provenancedialog import Ui_ProvenanceDialog
from mapclient.core.provenance import reproducibility_info


class ProvenanceDialog(QDialog):
    """
    Dialog to display the provenance information.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_ProvenanceDialog()
        self._ui.setupUi(self)

        info = reproducibility_info()
        self._headers = ["Package", "Version", "Location"]
        for key in info.keys():
            if key == 'mapclient':
                table = self._ui.tableWidgetMAPClient
                content = {'mapclient': info[key]}
            elif key == 'plugins':
                table = self._ui.tableWidgetPlugin
                content = info[key]
            elif key == 'packages':
                table = self._ui.tableWidgetPackage
                content = info[key]
            else:
                continue

            self._add_table_content(table, content)

    def _add_table_content(self, table, content):
        table.setColumnCount(len(self._headers))
        table.setRowCount(len(content))
        table.verticalHeader().setVisible(False)

        table.setHorizontalHeaderLabels(self._headers)

        for row, i in enumerate(content):
            item_1 = QTableWidgetItem(i)
            item_2 = QTableWidgetItem(content[i]["version"])
            item_3 = QTableWidgetItem(content[i]["location"])
            table.setItem(row, 0, item_1)
            table.setItem(row, 1, item_2)
            table.setItem(row, 2, item_3)

        table.resizeColumnsToContents()
