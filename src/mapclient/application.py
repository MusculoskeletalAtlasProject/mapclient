#!/usr/bin/env python
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
from __future__ import absolute_import
import os
import ctypes
import argparse

import sys, locale
import logging
from logging import handlers

# import matplotlib

# Set toolbox settings here
# matplotlib.use('Qt4Agg')
# matplotlib.rcParams['backend.qt4']='PySide'

os.environ['ETS_TOOLKIT'] = 'qt4'
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
    """
    Initialise logger settings and information formatting
    """

    logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d/%m/%Y - %H:%M:%S')
    logging.addLevelName(29, 'PLUGIN')

    rotatingFH = handlers.RotatingFileHandler(log_path, mode='a', maxBytes=5000000, backupCount=9)
    rotatingFH.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y - %H:%M:%S')
    rotatingFH.setFormatter(file_formatter)
    logging.getLogger().addHandler(rotatingFH)
    rotatingFH.doRollover()


def programme_header():
    """
    Display program header
    """
    programHeader = '   {0} (version {1})   '.format(info.APPLICATION_NAME, info.ABOUT['version'])
    logger.info('-' * len(programHeader))
    logger.info(programHeader)
    logger.info('-' * len(programHeader))


# This method starts MAP Client
def windows_main(app_args):
    """
    Initialise common settings and check the operating environment before starting the application.
    """
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
    programme_header()

    logger.info('Setting toolbox settings for matplotlib and enthought to: qt4')

    try:
        from opencmiss.zinc.context import Context
        Context("MAP")
        logger.info('OpenCMISS-Zinc is available.')
    except ImportError:
        logger.warning('OpenCMISS-Zinc is not available.')

    try:
        from opencmiss.iron import iron
        logger.info('OpenCMISS-Iron is available.')
    except ImportError:
        logger.warn('OpenCMISS-Iron is not available.')

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()

    from mapclient.view.mainwindow import MainWindow
    window = MainWindow(model)
    window.show()

    # Run Checks
    if not window.checkApplicationSetup():
        window.setupApplication()

        if not window.checkApplicationSetup():
            window.showOptionsDialog(current_tab=1)

    window.loadPlugins()

    if app_args.workflow:
        window.openWorkflow(app_args.workflow)

    if app_args.execute:
        wm = model.workflowManager()
        if wm.canExecute():
            window.execute()
        else:
            logger.error('Could not execute workflow.')

    return app.exec_()


class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)


def non_gui_main(app_args):
    locale.setlocale(locale.LC_ALL, '')

#     from optparse import OptionParser
    from PySide import QtGui
#     app = QtCore.QCoreApplication(sys.argv)
    app = QtGui.QApplication(sys.argv)
    logging.basicConfig(level='DEBUG')

    info.setApplicationsSettings(app)

    old_stdout = sys.stdout
    sys.stdout = ConsumeOutput()
#     sys.stdout = redirectstdout = ConsumeOutput()
    programme_header()
    sys.stdout = old_stdout

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()
    model.readSettings()

    wm = model.workflowManager()
    pm = model.pluginManager()

    pm.load()
    try:
        wm.load(app_args.workflow)
    except:
        logger.error('Not a valid workflow location: {0}'.format(app_args.workflow))
        sys.exit(-1)

    wm.registerDoneExecutionForAll(wm.execute)

    if wm.canExecute():
        wm.execute()
    else:
        logger.error('Could not execute workflow.')

    # Possibly don't need to run app.exec_()
    return app.quit()


def main():
    parser = argparse.ArgumentParser(prog=info.APPLICATION_NAME)
    parser.add_argument("-x", "--execute", action="store_true", help="execute a workflow")
    parser.add_argument("--headless", action="store_true",
                        help="operate in headless mode, without a gui.  Requires a location of a workflow to be set")
    parser.add_argument("-w", "--workflow", help="location of workflow")
    args = parser.parse_args()

    if args.headless and args.workflow is None:
        parser.print_help()
        sys.exit(-2)

    if args.headless and args.workflow:
        sys.exit(non_gui_main(args))
    else:
        sys.exit(windows_main(args))

if __name__ == '__main__':
    main()