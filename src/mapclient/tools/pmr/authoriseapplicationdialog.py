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
import webbrowser

from PySide2 import QtCore, QtWidgets

from mapclient.tools.pmr.ui_authoriseapplicationdialog import Ui_AuthoriseApplicationDialog

from mapclient.tools.pmr.settings.general import PMR
from mapclient.tools.pmr.core import TokenHelper

logger = logging.getLogger(__name__)


class AuthoriseApplicationDialog(QtWidgets.QDialog):
    """
    Dialog for authorising the application.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_AuthoriseApplicationDialog()
        self._ui.setupUi(self)

        pmr_info = PMR()
        client_tokens = pmr_info.get_client_token_kwargs()
        self._helper = TokenHelper(
            client_key=client_tokens['client_key'],
            client_secret=client_tokens['client_secret'],
            site_url=pmr_info.host(),
        )

    def event(self, event):
        result = QtWidgets.QDialog.event(self, event)
        if event.type() == QtCore.QEvent.ShowToParent:
            answer = QtWidgets.QMessageBox.question(self, 'Permission Required',
                                                    'Can the MAP Client access PMR on your behalf?',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.Yes)
            if answer == QtWidgets.QMessageBox.No:
                self.reject()
            else:
                self._show_pmr()

        return result

    def _show_pmr(self):

        try:
            self._helper.get_temporary_credentials()
        except ValueError:
            logger.info('Invalid Client Credentials: Failed to retrieve temporary credentials.')
            QtWidgets.QMessageBox.information(self, 'Invalid Client Credentials',
                                              'Failed to retrieve temporary credentials.')
            return

        url = self._helper.get_authorize_url()
        webbrowser.open(url)

    def accept(self):
        if len(self._ui.tokenLineEdit.text()) > 0:
            self._register()

        QtWidgets.QDialog.accept(self)

    def _register(self):
        pmr_info = PMR()

        verifier = self._ui.tokenLineEdit.text()
        self._helper.set_verifier(verifier)

        try:
            token_credentials = self._helper.get_token_credentials()
        except ValueError:
            logger.info('Invalid Verifier: Failed to retrieve token access with verification code.')
            QtWidgets.QMessageBox.information(self, 'Invalid Verifier',
                'Failed to retrieve token access with verification code.')
            return False

        logger.debug('token: %r', token_credentials)

        pmr_info.update_token(**token_credentials)

        return True
