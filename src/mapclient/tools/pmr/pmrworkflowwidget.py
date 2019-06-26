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
import re

from PySide2 import QtWidgets, QtCore

from mapclient.tools.pmr.ui_pmrworkflowwidget import Ui_PMRWorkflowWidget
from mapclient.view.utils import handle_runtime_error, set_wait_cursor
from mapclient.tools.pmr.pmrtool import PMRTool, search_domains, \
    workflow_search_string, ontological_search_string
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog
from pmr2.client.client import Client
from mapclient.tools.pmr.settings import general
from mapclient.tools.pmr.settings.general import PMR


class PMRWorkflowWidget(QtWidgets.QWidget):
    """
    A Widget for importing and exporting to and from PMR.
    """

    def __init__(self, use_external_git, parent=None):
        super(PMRWorkflowWidget, self).__init__(parent)
        self._ui = Ui_PMRWorkflowWidget()
        self._ui.setupUi(self)

        pmr_info = PMR()
        self._pmrTool = PMRTool(pmr_info, use_external_git)

        self._termLookUpLimit = 32

        self._timer = QtCore.QTimer()
        self._timer.setInterval(500)

        self._busy_waiting = False
        self._ontological_search = False

        word_list = ['pending ...']
        self._list_model = OWLTermsListModel(word_list)

#         self._client = Client(site=pmr_target, use_default_headers=True)

        self._makeConnections()

        self._ui.comboBoxSearch.clear()
        self._ui.comboBoxSearch.addItems(search_domains)

        self._updateUi()

    def _updateUi(self):
        if self._pmrTool.hasAccess():
            self._ui.labelLink.setText('<a href="mapclient.deregister">deregister</a>')
        else:
            self._ui.labelLink.setText('<a href="mapclient.register">register</a>')

    def _makeConnections(self):
        self._ui.pushButtonSearch.clicked.connect(self._searchClicked)
        self._ui.pushButtonImport.clicked.connect(self._importClicked)
        self._ui.pushButtonExport.clicked.connect(self._exportClicked)
        self._ui.labelLink.linkActivated.connect(self._linkActivated)
        self._ui.listWidgetResults.itemClicked.connect(self._searchResultClicked)
        self._ui.lineEditSearch.textEdited.connect(self._searchTextEdited)
        self._timer.timeout.connect(self._queryRepository)
        self._ui.comboBoxSearch.currentIndexChanged.connect(self._searchTypeChanged)

    def _initialiseCompleter(self):
        completer = QtWidgets.QCompleter(self._ui.lineEditSearch)
        completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setModel(self._list_model)
        completer.setCompletionColumn(0)
        completer.setCompletionRole(QtCore.Qt.DisplayRole)

        return completer

    def _searchTypeChanged(self, index):
        text = self._ui.comboBoxSearch.currentText()
        if text == ontological_search_string:
            self._ontological_search = True
            completer = self._initialiseCompleter()
            self._ui.lineEditSearch.setCompleter(completer)
        else:
            self._ontological_search = False
            self._ui.lineEditSearch.setCompleter(None)

    def _searchTextEdited(self, new_text):
        if self._ontological_search and len(new_text) and not self._busy_waiting:
            if self._timer.isActive():
                QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self._timer.start()

    def _queryRepository(self):
        self._timer.stop()
        self._busy_waiting = True
        search_text = self._ui.lineEditSearch.text()
        pmr_target = general.PMR().host()
        target = pmr_target + '/pmr2_ricordo/owlterms' + '/%s/%d' % (search_text, self._termLookUpLimit)
        client = Client(site=pmr_target, use_default_headers=True)
        state = client(target=target)  # , data=json.dumps({'actions': {'search': 1}, 'fields': {'simple_query': 'femur'}}))  # , endpoint='ricordo', data='femur')
        response = state.value()
        descriptions = ['%s [%s]' % (line[0], line[1].split('#')[-1]) for line in response['results']]
        self._list_model.removeRows(0, self._list_model.rowCount())
        self._list_model.insertRows(0, len(descriptions), descriptions)
        self._busy_waiting = False

    def _searchResultClicked(self, item):
        r = item.data(QtCore.Qt.UserRole)
        if 'source' in r:
            self._ui.lineEditWorkspace.setText(r['source'])
        elif 'href' in r:
            self._ui.lineEditWorkspace.setText(r['href'])

    def _linkActivated(self, link):
        if link == 'mapclient.register':
            dlg = AuthoriseApplicationDialog(self)
            dlg.setModal(True)
            dlg.exec_()
            self._updateUi()
        elif link == 'mapclient.deregister':
            self._pmrTool.deregister()
            self._updateUi()

    def _searchClicked(self):
        self._doSearch(self._ui.comboBoxSearch.currentText())

    def _importClicked(self):
        pass

    def _exportClicked(self):
        pass

    def setSearchDomain(self, domain=['all', ]):
        self._domain = []
        if type(domain) is not list:
            domain = [domain]

        if len(domain) and domain[0] == 'all':
            domain = search_domains

        for subdomain in domain:
            if subdomain in search_domains:
                self._domain.append(subdomain)

        if len(self._domain):
            self._ui.comboBoxSearch.clear()
            for subdomain in self._domain:
                self._ui.comboBoxSearch.addItem(subdomain)

    def setExport(self, visible=True):
        if visible:
            self._ui.pushButtonExport.show()
        else:
            self._ui.pushButtonExport.hide()

    def setImport(self, visible=True):
        if visible:
            self._ui.pushButtonImport.show()
        else:
            self._ui.pushButtonImport.hide()

    def workspaceUrl(self):
        return self._ui.lineEditWorkspace.text()

    def setWorkspaceUrl(self, url):
        self._ui.lineEditWorkspace.setText(url)

    @handle_runtime_error
    @set_wait_cursor
    def _doSearch(self, search_type):
        # Set pmrlib to go
        self._ui.listWidgetResults.clear()

        # fix up known terms to be full blown uri
        search_text = self._ui.lineEditSearch.text()
        if True:
            search_text = self._ui.lineEditSearch.text()
            label_re = re.compile('\[([\w_\d]+)\]')
            re_result = label_re.search(search_text)
            if re_result:
                search_text = re_result.group(1)
#         search_terms = search_text.split()
#         for term in search_terms:
#             rdfterm = self._annotationTool.rdfFormOfTerm(term)
#             if rdfterm:
#                 search_text = search_text + ' ' + rdfterm[1:-1]
        results = self._pmrTool.search(search_text, search_type)

        if search_type == workflow_search_string:
            results_list = results['results']
            for r in results_list:
                item = QtWidgets.QListWidgetItem(r['obj']['title'], self._ui.listWidgetResults)
                item.setData(QtCore.Qt.UserRole, r)
        elif search_type == ontological_search_string:
            if type(results) is dict:
                return

            for r in results:
                label = r['label']
                for sr in r['items']:
                    item = QtWidgets.QListWidgetItem(sr['title'] + ' [%s, %s]' % (sr['value'], label), self._ui.listWidgetResults)
                    tool_tip = 'Workspace title: %s, Ontological term: %s, Target: %s' % (sr['title'], label, sr['href'])
                    item.setToolTip(tool_tip)
                    item.setData(QtCore.Qt.UserRole, sr)

        else:
            for r in results:
                if 'title' in r and r['title']:
                    item = QtWidgets.QListWidgetItem(r['title'], self._ui.listWidgetResults)
                else:
                    item = QtWidgets.QListWidgetItem(r['target'], self._ui.listWidgetResults)
                item.setData(QtCore.Qt.UserRole, r)


class OWLTermsListModel(QtCore.QAbstractListModel):

    def __init__(self, list_in, parent=None, *args, **kwargs):
        super(OWLTermsListModel, self).__init__()
        self._list_in = list_in

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._list_in)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return self._list_in[index.row()]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            self._list_in[row] = value

    def insertRows(self, position, rows, newList, parent=QtCore.QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)

        self._list_in = newList

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for _ in range(rows):
            value = self._list_in[position]
            self._list_in.remove(value)

        self.endRemoveRows()
        return True
