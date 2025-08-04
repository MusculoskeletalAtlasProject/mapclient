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
import faulthandler

import locale

import logging
import zipfile
from logging import handlers

from mapclient.core.exitcodes import HEADLESS_MODE_WITH_NO_WORKFLOW, INVALID_WORKFLOW_LOCATION_GIVEN
from mapclient.core.utils import is_frozen, find_file
from mapclient.settings.definitions import INTERNAL_WORKFLOWS_ZIP, INTERNAL_WORKFLOWS_AVAILABLE, INTERNAL_WORKFLOW_DIR, UNSET_FLAG, PREVIOUS_WORKFLOW, AUTOLOAD_PREVIOUS_WORKFLOW
from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE

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
def windows_main(workflow, execute_now):
    """
    Initialise common settings and check the operating environment before starting the application.
    """
    if sys.platform == 'win32':
        my_app_id = 'MusculoSkeletal.MAPClient'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    faulthandler.enable()
    # import the locale, and set the locale. This is used for
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')

    from PySide6 import QtWidgets
    from mapclient.splashscreen import SplashScreen

    app = QtWidgets.QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()
    splash.showMessage("Loading settings ...", 5)
    info.set_applications_settings(app)

    log_path = get_log_location()
    initialise_logger(log_path)
    program_header()

    logger.info('Setting toolbox settings for matplotlib and enthought to: qt')

    splash.showMessage('Loading cmlibs.zinc ...', 10)
    try:
        import cmlibs.zinc.context
        logger.info('Zinc is available.')
    except ImportError:
        logger.warning(' *** Zinc is not available ***')

    splash.showMessage('Creating application ...', 20)
    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()

    splash.showMessage('Creating main window ...', 30)
    from mapclient.view.mainwindow import MainWindow
    window = MainWindow(model)

    # Run Checks
    if not window.check_application_setup():
        window.setup_application()

        splash.showMessage('Check application setup ...', 40)
        if not window.check_application_setup():
            window.show_options_dialog(current_tab=1)

    splash.showMessage('Loading packages ...', 50)
    window.load_packages()
    splash.showMessage('Loading plugins ...', 60)
    window.load_plugins()

    splash.showMessage('Loading internal workflow ...', 70)
    om = model.optionsManager()
    _prepare_internal_workflows(om)
    if om.getOption(AUTOLOAD_PREVIOUS_WORKFLOW):
        workflow = _load_previous_workflow(workflow, om)

    window.show()
    wm = model.workflowManager()
    if workflow and not wm.is_restricted(workflow):
        splash.showMessage('Opening workflow ...', 80)
        logger.info(f"Opening workflow: {workflow}")
        window.open_workflow(workflow)
    elif workflow:
        logger.info(f"Not opening workflow '{workflow}', this workflow is already in use.")

    window.start_metrics()
    if execute_now:
        splash.showMessage('Executing workflow ...', 90)
        if wm.canExecute() == 0:
            window.execute()
        else:
            logger.error(f'Could not execute workflow, reason: "{wm.execute_status_message()}"')

    splash.showMessage('Ready ...', 100)
    splash.finish(window)
    return app.exec()


def _get_default_internal_workflow(om):
    internal_workflow_dir = om.getOption(INTERNAL_WORKFLOW_DIR)
    default_workflow = os.path.join(internal_workflow_dir, "default_workflow.txt")
    if os.path.isfile(default_workflow):
        with open(default_workflow) as f:
            lines = f.readlines()

        return find_file(DEFAULT_WORKFLOW_PROJECT_FILENAME, os.path.join(internal_workflow_dir, lines[0].rstrip()))

    return find_file(DEFAULT_WORKFLOW_PROJECT_FILENAME, internal_workflow_dir)


def _load_previous_workflow(workflow, om):
    previous_workflow_dir = om.getOption(PREVIOUS_WORKFLOW)
    if previous_workflow_dir != UNSET_FLAG:
        workflow_file = find_file(DEFAULT_WORKFLOW_PROJECT_FILENAME, previous_workflow_dir)
    else:
        if not om.getOption(INTERNAL_WORKFLOWS_AVAILABLE):
            return

        workflow_file = _get_default_internal_workflow(om)

    # Set workflow to internal workflow if None is currently present.
    if workflow is None and workflow_file is not None:
        # Should definitely have a workflow now.
        workflow = os.path.dirname(workflow_file)

    return workflow


def _prepare_internal_workflows(om):
    # Determine if we have an internal workflow.
    if is_frozen():
        internal_workflows_zip = os.path.join(sys._MEIPASS, INTERNAL_WORKFLOWS_ZIP)
    else:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        internal_workflows_zip = os.path.realpath(os.path.join(file_dir, '..', INTERNAL_WORKFLOWS_ZIP))

    if os.path.isfile(internal_workflows_zip):
        # We have an internal workflow set the option as active.
        om.setOption(INTERNAL_WORKFLOWS_AVAILABLE, True)

        # Work out internal workflow directory and create if it doesn't exist.
        internal_workflow_dir = om.getOption(INTERNAL_WORKFLOW_DIR)
        if internal_workflow_dir == UNSET_FLAG or not os.path.isdir(internal_workflow_dir):
            internal_workflow_dir = get_default_internal_workflow_dir()
            if not os.path.isdir(internal_workflow_dir):
                logger.info(f"Creating internal workflow(s) directory '{internal_workflow_dir}'")
                os.mkdir(internal_workflow_dir)

        om.setOption(INTERNAL_WORKFLOW_DIR, internal_workflow_dir)

        # Test if a workflow is present.
        workflow_file = find_file(DEFAULT_WORKFLOW_PROJECT_FILENAME, internal_workflow_dir)
        if workflow_file is None:
            # No workflow exists in the workflow directory so we will
            # unzip the stored workflow(s) into this location.
            logger.info("Decompressing internal workflow(s) ...")
            archive = zipfile.ZipFile(internal_workflows_zip)
            archive.extractall(f"{internal_workflow_dir}")

    else:
        om.setOption(INTERNAL_WORKFLOWS_AVAILABLE, False)


class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)


def _prepare_sans_gui_app(app):
    logging.basicConfig(level='INFO')

    info.set_applications_settings(app)

    old_stdout = sys.stdout
    sys.stdout = ConsumeOutput()
    #     sys.stdout = redirectstdout = ConsumeOutput()

    log_path = get_log_location()
    initialise_logger(log_path)
    program_header()
    sys.stdout = old_stdout

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()
    model.readSettings()

    return model


def sans_gui_main(workflow):
    locale.setlocale(locale.LC_ALL, '')

    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    model = _prepare_sans_gui_app(app)

    wm = model.workflowManager()
    pm = model.pluginManager()
    pam = model.package_manager()
    om = model.optionsManager()

    pam.load()
    pm.load()

    _prepare_internal_workflows(om)

    class FacadeMainWindow:

        def __init__(self, _model):
            self._model = _model

        def model(self):
            return self._model

    try:
        wm.scene().setMainWindow(FacadeMainWindow(model))
        wm.load(workflow)
    except:
        logger.error('Not a valid workflow location: "{0}"'.format(workflow))
        sys.exit(INVALID_WORKFLOW_LOCATION_GIVEN)

    wm.registerDoneExecutionForAll(wm.execute)

    if wm.canExecute() == 0:
        wm.execute()
    else:
        logger.error(f'Could not execute workflow, reason: "{wm.execute_status_message()}"')

    # Possibly don't need to run app.exec_()
    return app.quit()


def _parse_prepare_user_specified_environment_args():
    parser = argparse.ArgumentParser(prog=f"{info.APPLICATION_NAME}_use".lower(),
                                     description="An application to create and setup a separate configuration location for running MAP Client.")
    parser.add_argument("base_dir", help="Sets the base directory for the setup, must exist.")
    parser.add_argument("-d", "--directory", action='append', help="Specify a plugin directory, can be used multiple times.")

    return parser.parse_args()


def user_specified_environment_main():
    locale.setlocale(locale.LC_ALL, '')

    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    logging.basicConfig(level='INFO')

    info.set_applications_settings(app)

    args = _parse_prepare_user_specified_environment_args()
    if not os.path.isdir(args.base_dir):
        sys.exit(1)

    config_dir = os.path.join(args.base_dir, ".config")
    os.environ[APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE] = config_dir

    if args.directory is not None:
        model = _prepare_sans_gui_app(app)
        model.readSettings()
        pm = model.pluginManager()
        directories = pm.directories()
        for d in args.directory:
            if os.path.isdir(d) and d not in directories:
                directories.append(d)

        pm.setDirectories(directories)
        model.writeSettings()

    print(f"Set environment variable '{APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}' to '{config_dir}' to use application with these settings.")
    if sys.platform == "win32":
        print(f'set {APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}="{config_dir}"')
    else:
        print(f'export {APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}="{config_dir}"')


def main():
    parser = argparse.ArgumentParser(prog=info.APPLICATION_NAME)
    parser.add_argument("-x", "--execute", action="store_true", help="execute a workflow")
    parser.add_argument("-s", "--headless", action="store_true",
                        help="operate in headless mode, without a gui.  Requires a location of a workflow to be set")
    parser.add_argument("-w", "--workflow", help="location of workflow")
    args = parser.parse_args(sys.argv[1:])

    if args.headless and args.workflow is None:
        parser.print_help()
        sys.exit(HEADLESS_MODE_WITH_NO_WORKFLOW)

    if args.headless and args.workflow:
        sys.exit(sans_gui_main(args.workflow))
    else:
        sys.exit(windows_main(args.workflow, args.execute))


if __name__ == '__main__':
    main()
