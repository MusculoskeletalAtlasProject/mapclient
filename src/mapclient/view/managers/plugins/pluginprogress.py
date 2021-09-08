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
import os, zipfile, requests
from PySide2 import QtWidgets

from mapclient.view.managers.plugins.ui.ui_pluginprogress import Ui_DownloadProgress


class PluginProgress(QtWidgets.QDialog):
    """
    Displays download and extraction progress of plugins from GitHub repository.
    """

    def __init__(self, plugins, directory, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_DownloadProgress()
        self._ui.setupUi(self)
        self._makeConnections()

        self._directory = directory
        self._plugins = plugins
        self._filenames = {}
        self._totalBytes = 0
        self._download_strings = ['Downloading %d of %d plugins...', 'Extracting %d of %d plugins...']
        self._ui.progressBar.setMaximum(len(plugins) * 50)
        self._ui.progressBar.setValue(0)

    def _makeConnections(self):
        self._ui.cancelDownload.clicked.connect(self.downloadCancelled)

    def downloadCancelled(self):
        for filename in self._filenames:
            if os.path.exists(filename):
                os.remove(filename)
        self.close()

    def run(self):
        downloaded = 0
        url_no = 1
        for plugin in list(self._plugins.keys()):
            self._ui.label.setText(self._download_strings[0] % (url_no, len(self._plugins)))
            self._filenames[plugin] = plugin.lower().split(' ')
            filename = ''
            for part in self._filenames[plugin]:
                filename = filename + part
            self._filenames[plugin] = filename

            rq = requests.get(self._plugins[plugin]['location'])
            if not rq.ok:
                ret = QtWidgets.QMessageBox.critical(self, 'Error', '\n There was a problem downloading the following plugin:  ' + plugin + '\n\n Please check your internet connection.\t', QtGui.QMessageBox.Ok)
            self._totalBytes += int(rq.headers['Content-length'])
            with open(os.path.join(self._directory, self._filenames[plugin] + '.zip'), "wb") as zFile:
                for chunk in rq.iter_content(1):
                    zFile.write(chunk)
                    downloaded += len(chunk)
                    progress = downloaded / self._totalBytes
                    self._ui.progressBar.setValue(int(progress * url_no * 40))
            url_no += 1

        file_no = 1
        for plugin in self._plugins:
            self._ui.label.setText(self._download_strings[1] % (file_no, len(self._plugins)))
            zfobj = zipfile.ZipFile(os.path.join(self._directory, self._filenames[plugin] + '.zip'), 'r')
            zfobj.extractall(self._directory)
            self._ui.progressBar.setValue(self._ui.progressBar.value() + 5)
            zfobj.close()
            os.remove(os.path.join(self._directory, self._filenames[plugin] + '.zip'))
            self._ui.progressBar.setValue(self._ui.progressBar.value() + 5)
            file_no += 1
        self.close()
