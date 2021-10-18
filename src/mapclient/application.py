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
import os
import sys
import ctypes
import argparse

import locale

import logging
import zipfile
from logging import handlers

from mapclient.core.utils import is_frozen, find_file
from mapclient.settings.definitions import INTERNAL_WORKFLOW_ZIP, INTERNAL_WORKFLOW_AVAILABLE, INTERNAL_WORKFLOW_DIR, UNSET_FLAG

os.environ['ETS_TOOLKIT'] = 'qt'
# With PEP366 we need to conditionally import the settings module based on
# whether we are executing the file directly of indirectly.  This is my
# workaround.
if __package__:
    from .settings import info
    from .settings.general import get_log_location, get_default_internal_workflow_dir
else:
    from mapclient.settings import info
    from mapclient.settings.general import get_log_location, get_default_internal_workflow_dir

logger = logging.getLogger('mapclient.application')


def initialise_logger(log_path):
    """
    Initialise logger settings and information formatting
    """

    logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                        datefmt='%d/%m/%Y - %H:%M:%S')
    logging.addLevelName(29, 'PLUGIN')

    rotating_fh = handlers.RotatingFileHandler(log_path, mode='a', maxBytes=5000000, backupCount=9)
    rotating_fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s.%(msecs).03d - %(name)s - %(levelname)s - %(message)s',
                                       datefmt='%d/%m/%Y - %H:%M:%S')
    rotating_fh.setFormatter(file_formatter)
    logging.getLogger().addHandler(rotating_fh)
    rotating_fh.doRollover()


def program_header():
    """
    Display program header
    """
    program_header_string = '   {0} (version {1})   '.format(info.APPLICATION_NAME, info.ABOUT['version'])
    logger.info('-' * len(program_header_string))
    logger.info(program_header_string)
    logger.info('-' * len(program_header_string))


# This method starts MAP Client
def windows_main(app_args):
    """
    Initialise common settings and check the operating environment before starting the application.
    """
    if sys.platform == 'win32':
        my_app_id = 'MusculoSkeletal.MAPClient'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    # import the locale, and set the locale. This is used for
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')

    from PySide2 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    # Set the default organisation name and application name used to store application settings
    info.set_applications_settings(app)

    log_path = get_log_location()
    initialise_logger(log_path)
    program_header()

    logger.info('Setting toolbox settings for matplotlib and enthought to: qt')

    try:
        from opencmiss.zinc.context import Context
        Context("MAP")
        logger.info('OpenCMISS-Zinc is available.')
    except ImportError:
        logger.warning(' *** OpenCMISS-Zinc is not available ***')

    try:
        from opencmiss.iron import iron
        # import opencmiss.utils.iron
        logger.info('OpenCMISS-Iron is available.')
    except ImportError:
        logger.warning(' *** OpenCMISS-Iron is not available ***')

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()

    from mapclient.view.mainwindow import MainWindow
    window = MainWindow(model)
    window.show()

    # Run Checks
    if not window.check_application_setup():
        window.setup_application()

        if not window.check_application_setup():
            window.show_options_dialog(current_tab=1)

    window.load_packages()
    window.load_plugins()

    om = model.optionsManager()
    prepare_internal_workflow(app_args, om)

    if app_args.workflow:
        window.open_workflow(app_args.workflow)

    if app_args.execute:
        wm = model.workflowManager()
        if wm.canExecute():
            window.execute()
        else:
            logger.error('Could not execute workflow.')

    return app.exec_()


def prepare_internal_workflow(app_args, om):
    # Determine if we have an internal workflow.
    if is_frozen():
        internal_workflow_zip = os.path.join(sys._MEIPASS, INTERNAL_WORKFLOW_ZIP)
    else:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        internal_workflow_zip = os.path.realpath(os.path.join(file_dir, '..', INTERNAL_WORKFLOW_ZIP))

    if os.path.isfile(internal_workflow_zip):
        # We have an internal workflow set the option as active.
        om.setOption(INTERNAL_WORKFLOW_AVAILABLE, True)

        # Work out internal workflow directory and create if it doesn't exist.
        internal_workflow_dir = om.getOption(INTERNAL_WORKFLOW_DIR)
        if internal_workflow_dir == UNSET_FLAG or not os.path.isdir(internal_workflow_dir):
            internal_workflow_dir = get_default_internal_workflow_dir()
            if not os.path.isdir(internal_workflow_dir):
                logger.info(f"Creating internal workflow(s) directory '{internal_workflow_dir}'")
                os.mkdir(internal_workflow_dir)

        om.setOption(INTERNAL_WORKFLOW_DIR, internal_workflow_dir)

        # Test if a workflow is present.
        workflow_file = find_file('workflow.conf', internal_workflow_dir)
        if workflow_file is None:
            # No workflow exists in the workflow directory so we will
            # unzip the stored workflow(s) into this location.
            logger.info("Decompressing internal workflow(s) ...")
            archive = zipfile.ZipFile(internal_workflow_zip)
            archive.extractall(f"{internal_workflow_dir}")

        # Should definitely have a workflow now.
        workflow_file = find_file('workflow.conf', internal_workflow_dir)
        default_workflow_directory = os.path.dirname(workflow_file)

        # Set workflow to internal workflow if None is currently present.
        if app_args.workflow is None:
            app_args.workflow = default_workflow_directory
            logger.info("Loading internal default workflow.")
    else:
        om.setOption(INTERNAL_WORKFLOW_AVAILABLE, False)


class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)


def sans_gui_main(app_args):
    locale.setlocale(locale.LC_ALL, '')

    from PySide2 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    logging.basicConfig(level='DEBUG')

    info.set_applications_settings(app)

    old_stdout = sys.stdout
    sys.stdout = ConsumeOutput()
    #     sys.stdout = redirectstdout = ConsumeOutput()
    program_header()
    sys.stdout = old_stdout

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()
    model.readSettings()

    wm = model.workflowManager()
    pm = model.pluginManager()
    pam = model.package_manager()
    om = model.optionsManager()

    pam.load()
    pm.load()

    prepare_internal_workflow(app_args, om)

    try:
        wm.load(app_args.workflow)
    except Exception:
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
        sys.exit(sans_gui_main(args))
    else:
        sys.exit(windows_main(args))


if __name__ == '__main__':
    main()
