'''
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
'''

from PySide import QtGui, QtCore
from PySide.QtCore import QThread, QObject, Signal

import time, subprocess, random, logging

from mapclient.view.managers.plugins.pluginprogress import PluginProgress
from mapclient.view.ui_progressdialog import Ui_ProgressDialog
from mapclient.core.utils import convertExceptionToMessage
from mapclient.view.managers.plugins.manager import PluginManager

logger = logging.getLogger(__name__)

class MySignal(QObject):
        sig = Signal(str)

class Thread(QThread):

    def __init__(self, env_dir, parent=None):
        QThread.__init__(self, parent)
        self.signal = MySignal()
        self.env_dir = env_dir

    def run(self):
        try:
            vem = PluginManager(self.env_dir)
            vem.setup()
            vem.addSitePackages()

        except Exception as e:
            message = convertExceptionToMessage(e)
            self.signal.sig.emit(message)

class VirtualEnvSetup(PluginProgress):

    def __init__(self, env_dir, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_ProgressDialog()
        self._ui.setupUi(self)
        self.setWindowTitle('Virtual Environment')
        self._ui.cancelDownload.setText('Ok')
        self._ui.progressBar.setValue(0)
        self._ui.progressBar.setMaximum(100)
        self.thread = Thread(env_dir)
        self._makeConnections()

    def _makeConnections(self):
        self.thread.terminated.connect(self.closeDialog)
        self.thread.signal.sig.connect(self.error)
        self._ui.cancelDownload.clicked.connect(self.closeDialog)

    def showEvent(self, *args, **kwargs):
        QtCore.QTimer.singleShot(500, self.run)
        return PluginProgress.showEvent(self, *args, **kwargs)

    def run(self):
        self.thread.start()
        self.animateProgress()
        self.validationStep()

    def animateProgress(self):
        self.started()
        damping = 1
        while self.thread.isRunning():
            time.sleep((random.randrange(20, 250) / 1000) * damping)
            self._ui.progressBar.setValue((self._ui.progressBar.value() + self._ui.progressBar.maximum()) / 4.0)
            damping += 0.05

        self.finished()

    def validationStep(self):
        while self._ui.progressBar.value() < self._ui.progressBar.maximum():
            time.sleep(0.01)
            self._ui.progressBar.setValue(self._ui.progressBar.value() + 1)
        self.complete()

    def error(self, data):
        self.close()
        logger.error('A problem occurred while setting up the virtual environment: \n\n' + data)
        QtGui.QMessageBox.warning(self, 'Setup Failed', 'A problem occurred while setting up the virtual environment: \n\n' + data, QtGui.QMessageBox.Ok)

    def started(self):
        logger.info('Setting up Virtual Environment. Please wait...')
        self._ui.label.setText('Setting up Virtual Environment. Please wait...')
        self._ui.cancelDownload.setEnabled(False)
        self._ui.progressBar.setValue(0)

    def finished(self):
        logger.info('Validating successful Virtual Environment setup...')
        self._ui.label.setText('Validating successful Virtual Environment setup...')

    def complete(self):
        logger.info('Virtual Environment successfully setup.')
        self._ui.label.setText('Virtual Environment successfully setup.')
        self._ui.cancelDownload.setEnabled(True)

    def closeDialog(self):
        self.close()


class InstallDependencies(PluginProgress):

    def __init__(self, packages_to_install, virt_env_dir, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_ProgressDialog()
        self._ui.setupUi(self)
        self.count = 0
        self._virt_env_dir = virt_env_dir
        self._packages_to_install = packages_to_install
        self.setWindowTitle('Installing Packages')
        self._ui.progressBar.setValue(0)
        self._ui.progressBar.setMaximum(100)
        self._ui.label.setText('Installing Packages...')
        self._makeConnections()

    def _makeConnections(self):
        self._ui.cancelDownload.clicked.connect(self.cancelInstallation)

    def cancelInstallation(self):
        for i in range(0, self.count - 1):
            try:
                subprocess.check_call([self._virt_env_dir + '\Scripts\python.exe', self._virt_env_dir + '\Scripts\pip.exe', 'uninstall', self._packages_to_install], shell=True)
            except Exception as e:
                message = convertExceptionToMessage(e)
                logger.info('Could not uninstall "' + self._packages_to_install[i] + '" package.')
                logger.info('Reason: ' + message)

    def run(self):
        print 'bad run'
        python_dir = self._virt_env_dir + '\Scripts\python.exe'
        pip_dir = self._virt_env_dir + '\Scripts\pip.exe'
        logs_dir = self._virt_env_dir[:-13] + '\logs'

        self._ui.label.setText('Searching for packages in pip index...')
        self._ui.progressBar.setMaximum(len(self._packages_to_install))
        found_packages = []
        not_found_packages = []
        for package in self._packages_to_install:
            self._ui.label.setText('Searching for "' + package + '" package...')
            try:
                output = subprocess.check_output([python_dir, pip_dir, 'search', package], shell=True)
                found_packages += [package]
            except Exception as e:
                not_found_packages += [package]
            self._ui.progressBar.setValue(self._ui.progressBar.value() + 1)

        self._ui.progressBar.reset()
        self._ui.progressBar.setMaximum(20 * len(found_packages))
        unsuccessful_installs = {}
        for package in found_packages:
            self.count += 1
            self._ui.label.setText('Installing "' + package + '" package...')
            for i in range(0, 10):
                time.sleep((random.randrange(0, 100) / 1000))
                self._ui.progressBar.setValue(self._ui.progressBar.value() + 1.5)
            try:
                with open(logs_dir + 'package_install_report_' + package + '.log', 'w') as file_out:
                    subprocess.check_call([python_dir, pip_dir, 'install', package], shell=True, stdout=file_out, stderr=file_out)
            except Exception as e:
                unsuccessful_installs[package] = convertExceptionToMessage(e)
                logger.warning('"' + package + '" dependency could not be installed.')
                logger.warning('Reason: ' + unsuccessful_installs[package])
            for i in range(0, 5):
                time.sleep(0.004)
                self._ui.progressBar.setValue(self._ui.progressBar.value() + 1)

        while self._ui.progressBar.value() < self._ui.progressBar.maximum():
            time.sleep(0.004)
            self._ui.progressBar.setValue(self._ui.progressBar.value() + 1)

        return unsuccessful_installs
