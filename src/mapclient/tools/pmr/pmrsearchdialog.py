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

from mapclient.tools.annotation.annotationtool import AnnotationTool
from mapclient.tools.pmr.pmrtool import PMRTool, PMRToolError
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog
from mapclient.tools.pmr.ui_pmrsearchdialog import Ui_PMRSearchDialog

from mapclient.view.utils import set_wait_cursor
from mapclient.view.utils import handle_runtime_error
from mapclient.core.utils import convertExceptionToMessage
from mapclient.tools.pmr.settings.general import PMR

logger = logging.getLogger(__name__)


class PMRSearchDialog(QtWidgets.QDialog):
    """
    Dialog for managing interaction with PMR.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_PMRSearchDialog()
        self._ui.setupUi(self)

        pmr_info = PMR()
        self._pmrTool = PMRTool(pmr_info)
        self._annotationTool = AnnotationTool()

        self._makeConnections()

        self._updateUi()

    def _updateUi(self):
        if self._pmrTool.hasAccess():
            self._ui.loginStackedWidget.setCurrentIndex(1)
        else:
            self._ui.loginStackedWidget.setCurrentIndex(0)

    def _makeConnections(self):
        self._ui.searchButton.clicked.connect(self._searchClicked)
        self._ui.registerLabel.linkActivated.connect(self.register)
        self._ui.deregisterLabel.linkActivated.connect(self.deregister)

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

    def register(self, link):
        if link != 'mapclient.register':
            return

        dlg = AuthoriseApplicationDialog(self)
        dlg.setModal(True)
        dlg.exec_()

        self._updateUi()

    def deregister(self):
        self._pmrTool.deregister()
        self._updateUi()
