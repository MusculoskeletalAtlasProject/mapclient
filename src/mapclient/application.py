#!/usr/bin/env python
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
from __future__ import absolute_import
import ctypes

import os, sys, locale
import logging
from logging import handlers

# With PEP366 we need to conditionally import the settings module based on
# whether we are executing the file directly of indirectly.  This is my
# workaround.
if __package__:
    from .settings import info
    from .settings.general import getLogLocation
else:
    from mapclient.settings import info
    from mapclient.settings.general import getLogLocation

logger = logging.getLogger('mapclient.application')

def initialiseLogger(log_path):
    '''
    Initialise logger settings and information formatting
    '''

    logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d/%m/%Y - %H:%M:%S')
    logging.addLevelName(29, 'PLUGIN')

    rotatingFH = handlers.RotatingFileHandler(log_path, mode='a', maxBytes=5000000, backupCount=9)
    rotatingFH.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y - %H:%M:%S')
    rotatingFH.setFormatter(file_formatter)
    logging.getLogger().addHandler(rotatingFH)
    rotatingFH.doRollover()

#     logging.addLevelName(28, 'MSG')

#     ch = logging.StreamHandler()
#     ch.setLevel(28)
#     formatter = logging.Formatter('%(message)s')
#     ch.setFormatter(formatter)

#     logger.addHandler(ch)

def progheader():
    '''
    Display program header
    '''
    programHeader = '   MAP Client (version %s)   ' % info.ABOUT['version']
    logger.info('-' * len(programHeader))
    logger.info(programHeader)
    logger.info('-' * len(programHeader))

# This method starts MAP Client
def winmain():
    '''
    Initialise common settings and check the operating environment before starting the application.
    '''
    if sys.platform == 'win32':
        myappid = 'MusculoSkeletal.MAPClient'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # import the locale, and set the locale. This is used for
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')

    from PySide import QtGui
    app = QtGui.QApplication(sys.argv)

    # Set the default organisation name and application name used to store application settings
    info.setApplicationsSettings(app)

    log_path = getLogLocation()
    initialiseLogger(log_path)
    progheader()

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()

    from mapclient.view.mainwindow import MainWindow
    window = MainWindow(model)
    window.show()

    # Run Checks
    window.checkApplicationSetup()

    return app.exec_()

class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

def main():
    locale.setlocale(locale.LC_ALL, '')

    from optparse import OptionParser
    from PySide import QtCore
    app = QtCore.QCoreApplication(sys.argv)

    logging.basicConfig(level='DEBUG')

    # Set the default organisation name and application name used to store application settings
    QtCore.QCoreApplication.setOrganizationName(info.ORGANISATION_NAME)
    QtCore.QCoreApplication.setOrganizationDomain(info.ORGANISATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationName(info.APPLICATION_NAME)

    old_stdout = sys.stdout
    sys.stdout = redirectstdout = ConsumeOutput()
    progheader()
    sys.stdout = old_stdout
    versionstring = ''.join(redirectstdout.messages)

    progname = os.path.splitext(__file__)[0]
    usage = 'usage: {0} [options] workflow\n    Execute the given workflow'.format(progname)
    parser = OptionParser(usage, version=versionstring)
    options, args = parser.parse_args()

    print(sys.argv)
    print(options, args)

    # Possibly don't need to run app.exec_()
    sys.exit(app.quit())


if __name__ == '__main__':
    if len(sys.argv) == 1:  # No command line arguments
        sys.exit(winmain())
    else:
        main()
