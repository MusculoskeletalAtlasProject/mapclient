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
import logging

from PySide2 import QtCore, QtWidgets

from mapclient.tools.pmr.widgets.ui_searchwidget import Ui_SearchWidget
from mapclient.view.utils import handle_runtime_error, set_wait_cursor
from mapclient.tools.pmr.pmrtool import PMRToolError, PMRTool
from mapclient.core.utils import convertExceptionToMessage
from mapclient.tools.annotation.annotationtool import AnnotationTool
from mapclient.tools.pmr.settings.general import PMR

logger = logging.getLogger(__name__)


class SearchWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)
        self._ui = Ui_SearchWidget()
        self._ui.setupUi(self)

        pmr_info = PMR()
        self._pmrTool = PMRTool(pmr_info)
        self._annotationTool = AnnotationTool()

        self._makeConnections()

    def setPMRInfo(self, info):
        self._pmrTool.set_info(info)

    def setUseExternalGit(self, use_external_git):
        self._pmrTool.set_use_external_git(use_external_git)

    def _makeConnections(self):
        self._ui.searchButton.clicked.connect(self._searchClicked)
        self._ui.searchResultsListWidget.itemClicked.connect(self._itemClicked)

    def _itemClicked(self, item):
        data = item.data(QtCore.Qt.UserRole)
        if 'target' in data:
            self._ui.targetEdit.setText(data['target'])

    @handle_runtime_error
    @set_wait_cursor
    def _searchClicked(self):
        # Set pmrlib to go
        self._ui.searchResultsListWidget.clear()

        # fix up known terms to be full blown uri
        search_text = self._ui.searchLineEdit.text()
        search_terms = search_text.split()
        for term in search_terms:
            rdfterm = self._annotationTool.rdfFormOfTerm(term)
            if rdfterm:
                search_text = search_text + ' ' + rdfterm[1:-1]

        try:
            results = self._pmrTool.search(search_text)

            for r in results:
                if 'title' in r and r['title']:
                    item = QtWidgets.QListWidgetItem(r['title'], self._ui.searchResultsListWidget)
                else:
                    item = QtWidgets.QListWidgetItem(r['target'], self._ui.searchResultsListWidget)
                item.setData(QtCore.Qt.UserRole, r)
        except PMRToolError as e:
            message = convertExceptionToMessage(e)
            logger.warning('PMR Tool exception raised')
            logger.warning('Reason: {0}'.format(message))

    def getSelectedWorkspace(self):
        items = self._ui.searchResultsListWidget.selectedItems()
        for item in items:
            return item.data(QtCore.Qt.UserRole)


