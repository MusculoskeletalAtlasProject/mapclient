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

from PySide2 import QtCore, QtGui, QtWidgets

from mapclient.view.utils import handle_runtime_error, set_wait_cursor
from mapclient.exceptions import ClientRuntimeError

from mapclient.tools.pmr.widgets.ui_settingswidget import Ui_SettingsWidget
from mapclient.tools.pmr.dialogs.addhostdialog import AddHostDialog
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.settings.general import PMR


class SettingsWidget(QtWidgets.QWidget):

    hostChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self._ui = Ui_SettingsWidget()
        self._ui.setupUi(self)

        self._pmr_tool = PMRTool()
        self._model = QtGui.QStandardItemModel()
        self._updateModel()

        self._ui.hostListView.setModel(self._model)

        self._updateUi()
        self._makeConnections()

    def _makeConnections(self):
        self._ui.addPushButton.clicked.connect(self._addClicked)
        self._ui.removePushButton.clicked.connect(self._removeClicked)
        self._ui.hostListView.clicked.connect(self._updateUi)  # We are making clicking to be synonymous with selecting, OK I think for single selection mode
        self._ui.hostListView.addAction(self._ui.actionAddHost)
        self._ui.actionAddHost.triggered.connect(self._addClicked)
        self._model.itemChanged.connect(self._hostChanged)

    def _updateUi(self):
        self._ui.removePushButton.setEnabled(len(self._ui.hostListView.selectedIndexes()))

    def _updateModel(self):
        pmr_info = PMR()
        for instance in pmr_info.hosts():
            self.addHost(instance, instance == pmr_info.activeHost())

    def setUseExternalGit(self, use_external_git):
        self._pmr_tool.set_use_external_git(use_external_git)

    def transferModel(self):
        """
        Transfer the current status of the model into the PMR
        information object.
        """
        pmr_info = PMR()
        hosts = pmr_info.hosts()
        host_names_remove = [name for name in hosts]
        host_names_new = []
        active_host = None

        index = 0
        current_item = self._model.item(index)
        while current_item:
            current_host = current_item.text()
            if current_host in host_names_remove:
                host_names_remove.remove(current_host)
            else:
                host_names_new.append(current_host)

            if current_item.checkState() == QtCore.Qt.Checked:
                active_host = current_host

            index += 1
            current_item = self._model.item(index)

        pmr_info.setActiveHost(active_host)
        for host in host_names_remove:
            pmr_info.removeHost(host)
        for host in host_names_new:
            pmr_info.addHost(host)


    def _addClicked(self):
        dlg = AddHostDialog(self)

        dlg.setModal(True)
        if dlg.exec_():
            self.addHost(dlg.getHost())

    def _removeClicked(self):
        indexes = self._ui.hostListView.selectedIndexes()
        rm_index = indexes.pop()
        item = self._model.itemFromIndex(rm_index)
        pmr_info = PMR()
        pmr_info.removeHost(item.text())
        self._model.removeRow(rm_index.row())
#         item = self._model.takeItem(rm_index.row())

    def _whichHostChecked(self):
        index = 0
        current_item = self._model.item(index)
        while current_item:
            if current_item.checkState():
                return index
            index += 1
            current_item = self._model.item(index)

        return -1

    def _hostChanged(self, item):
        pmr_info = PMR()
        if not item.checkState():
            pmr_info.setActiveHost(None)
            self.hostChanged.emit(item.row())
            return

        index = 0
        current_item = self._model.item(index)
        self.blockSignals(True)
        while current_item:
            if current_item.checkState() and (current_item.row() != item.row()):
                current_item.setCheckState(QtCore.Qt.Unchecked)
            index += 1
            current_item = self._model.item(index)

        self.blockSignals(False)
        pmr_info.setActiveHost(item.text())
        self.hostChanged.emit(item.row())

    @handle_runtime_error
    @set_wait_cursor
    def addHost(self, host, active=False):
        try:
            # Look for duplicates
            host_item = QtGui.QStandardItem(host)
            same_items = self._model.findItems(host)
            if len(same_items):
                raise Exception('Host "{0}" already exists'.format(host))

            if self._pmr_tool.isValidHost(host):
                host_item.setCheckable(True)
                host_item.setCheckState(QtCore.Qt.Checked if active else QtCore.Qt.Unchecked)
                self._model.appendRow(host_item)
        except Exception as e:
            raise ClientRuntimeError(
                        'Error Adding Host', str(e))



