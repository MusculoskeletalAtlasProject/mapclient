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
import json
import multiprocessing
import os
import shutil
import sys
import ctypes
import argparse

import locale

import logging
from logging import handlers
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from mapclient.core.exitcodes import (HEADLESS_MODE_WITH_NO_WORKFLOW, INVALID_WORKFLOW_LOCATION_GIVEN, CONFIGURATION_MODE_WITH_NO_DEFINITIONS, USER_SPECIFIED_DIRECTORY,
                                      APP_SUCCESS, CONFIGURATION_MODE_NO_FILE, CONFIGURATION_MODE_NOT_IMPLEMENTED)
from mapclient.core.provenance import reproducibility_info
from mapclient.core.utils import is_frozen, find_file
from mapclient.core.workflow.workflowscene import create_from
from mapclient.settings.definitions import INTERNAL_WORKFLOWS_ZIP, INTERNAL_WORKFLOWS_AVAILABLE, INTERNAL_WORKFLOW_DIR, UNSET_FLAG, PREVIOUS_WORKFLOW, AUTOLOAD_PREVIOUS_WORKFLOW
from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE

os.environ['ETS_TOOLKIT'] = 'qt'
# With PEP366 we need to conditionally import the settings module based on
# whether we are executing the file directly of indirectly.  This is my
# workaround.
if __package__:
    from .settings import info
    from .settings.general import get_log_location, get_default_internal_workflow_dir, get_configuration_file
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


def _prepare_application():
    # import the locale, and set the locale. This is used for
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')

    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    info.set_applications_settings(app)
    log_path = get_log_location()
    initialise_logger(log_path)

    return app


# This method starts MAP Client
def windows_main(workflow, execute_now):
    """
    Initialise common settings and check the operating environment before starting the application.
    """
    if sys.platform == 'win32':
        my_app_id = 'MusculoSkeletal.MAPClient'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    from mapclient.splashscreen import SplashScreen

    app = _prepare_application()
    splash = SplashScreen()
    splash.show()
    splash.showMessage("Loading settings ...", 5)
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
            archive = ZipFile(internal_workflows_zip)
            archive.extractall(f"{internal_workflow_dir}")

    else:
        om.setOption(INTERNAL_WORKFLOWS_AVAILABLE, False)


class ConsumeOutput:
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

    def flush(self, *args, **kwargs):
        pass


def prepare_sans_gui_app(app):
    info.set_applications_settings(app)

    old_stdout = sys.stdout
    sys.stdout = ConsumeOutput()
    #     sys.stdout = redirectstdout = ConsumeOutput()

    program_header()
    sys.stdout = old_stdout

    from mapclient.core.mainapplication import MainApplication
    model = MainApplication()
    model.readSettings()

    return model


def _backup_file(file_path):
    return f"{file_path}.bak"


def _restore_backup(config_file):
    if os.path.isfile(config_file):
        os.remove(config_file)

    os.rename(_backup_file(config_file), config_file)


def sans_gui_main(workflow, import_settings=None, relocate=False):

    if workflow is None:
        return HEADLESS_MODE_WITH_NO_WORKFLOW

    app = _prepare_application()
    model = prepare_sans_gui_app(app)

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

    backed_up_config_files = []
    try:
        wm.scene().setMainWindow(FacadeMainWindow(model))
        if import_settings is not None:
            with ZipFile(import_settings) as archive:
                with TemporaryDirectory() as temp_dir:
                    archive.extractall(temp_dir)
                    source_steps_list = wm.list_steps(temp_dir)

                    target_steps_list = wm.list_steps(workflow)

                    all_present = all(item in target_steps_list for item in source_steps_list)
                    if all_present:

                        # Relocate step configurations if required.
                        if relocate:
                            source_steps = wm.load_steps(temp_dir)
                            for step in source_steps:
                                step.setLocation(os.path.dirname(import_settings))
                                step.relocateConfiguration(workflow)
                                config_file = get_configuration_file(temp_dir, step.getIdentifier())
                                with open(config_file, "w") as fh:
                                    fh.write(step.serialize())

                        # Make backups of target steps configurations and import new configuration.
                        for step_name, identifier in source_steps_list:
                            config_file = get_configuration_file(workflow, identifier)
                            new_config_file = get_configuration_file(temp_dir, identifier)
                            if os.path.isfile(config_file):
                                shutil.copy2(config_file, _backup_file(config_file))
                                shutil.copy2(new_config_file, config_file)
                                backed_up_config_files.append(config_file)

        wm.load(workflow)
    except:
        logger.error('Not a valid workflow location: "{0}"'.format(workflow))
        sys.exit(INVALID_WORKFLOW_LOCATION_GIVEN)

    wm.registerDoneExecutionForAll(wm.execute)

    if wm.canExecute() == 0:
        try:
            wm.execute()
        finally:
            for backed_up_file in backed_up_config_files:
                _restore_backup(backed_up_file)
    else:
        logger.error(f'Could not execute workflow, reason: "{wm.execute_status_message()}"')

    # Possibly don't need to run app.exec_()
    return app.quit()


def _user_specified_environment_main(base_dir, directories):
    app = _prepare_application()

    if not os.path.isdir(base_dir):
        return USER_SPECIFIED_DIRECTORY

    config_dir = os.path.join(base_dir, ".config")
    os.environ[APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE] = config_dir

    if directories is not None:
        model = prepare_sans_gui_app(app)
        # model.readSettings()
        pm = model.pluginManager()
        plugin_directories = pm.directories()
        for d in directories:
            if os.path.isdir(d) and d not in plugin_directories:
                plugin_directories.append(d)

        pm.setDirectories(plugin_directories)
        model.writeSettings()

    logger.info(f"Set environment variable '{APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}' to '{config_dir}' to use application with these settings.")
    if sys.platform == "win32":
        logger.info(f'set {APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}="{config_dir}"')
    else:
        logger.info(f'export {APPLICATION_ENVIRONMENT_CONFIG_DIR_VARIABLE}="{config_dir}"')

    return APP_SUCCESS


def _split_key_value_definition(text):
    index = text.find(":")
    if index == -1:
        return text, ""
    return text[:index], text[index + 1:]


def _config_maker_main(configuration_file, definitions, append):
    if configuration_file is None:
        logger.error("No configuration file specified.")
        return CONFIGURATION_MODE_NO_FILE

    if configuration_file and definitions is None:
        logger.error("No definitions set.")
        return CONFIGURATION_MODE_WITH_NO_DEFINITIONS

    app = _prepare_application()
    logger.info("Running config maker.")
    location = os.path.dirname(configuration_file)

    workflow_settings = {}
    required_steps = []
    for index, definition in enumerate(definitions):
        step_name, identifier = _split_key_value_definition(definition[0])

        if (step_name, identifier) not in required_steps:
            required_steps.append((step_name, identifier))
        key, value = _split_key_value_definition(definition[1])
        current_settings = workflow_settings.get(step_name, {})
        current_data = current_settings.get(identifier, [])
        current_data.append((key, value))
        current_settings[identifier] = current_data
        workflow_settings[step_name] = current_settings

    model = prepare_sans_gui_app(app)
    pm = model.pluginManager()
    wm = model.workflowManager()
    pm.load()
    logger.info("Loaded MAP Client plugins.")

    files_created = []

    wf = wm.create_empty_workflow(location)
    steps = create_from(wf, required_steps, None, location)
    files_created.append(wf.fileName())
    del wf
    logger.info("Created workflow.")

    not_implemented_occurred = False
    for index, step in enumerate(steps):
        step_configurations = workflow_settings[step.getName()]
        step_configuration = step_configurations[step.getIdentifier()]
        try:
            step.setConfiguration(step_configuration)
            current_config_file = get_configuration_file(location, step.getIdentifier())
            with open(current_config_file, "w") as fh:
                fh.write(step.serialize())

            files_created.append(current_config_file)
        except NotImplementedError:
            not_implemented_occurred = True
            logger.info(f"The step '{step.getName()}' does not support configuration making.")
            logger.info("This step does not implement the 'setConfiguration' method.")

    logger.info("Created workflow configuration files.")
    if not_implemented_occurred:
        logger.error("Not all steps defined support configuration making.")
        return CONFIGURATION_MODE_NOT_IMPLEMENTED

    provenance = reproducibility_info()
    provenance_file = os.path.join(location, "provenance.json")
    with open(provenance_file, "w") as f:
        f.write(json.dumps(provenance, default=lambda o: o.__dict__, sort_keys=True, indent=2))
    files_created.append(provenance_file)
    logger.info("Created provenance file.")

    zip_file = os.path.join(location, "workflow-settings.zip")

    with ZipFile(zip_file, "w") as fh:
        for f in files_created:
            archive_name = os.path.relpath(f, location)
            fh.write(f, arcname=archive_name)
            os.remove(f)

    logger.info("Successfully created workflow archive.")

    return APP_SUCCESS


def _common_workflow_args(parser):
    parser.add_argument("-x", "--execute", action="store_true", help="Execute a workflow.")
    parser.add_argument("-w", "--workflow", help="Location of workflow.")
    parser.add_argument("-i", "--import-settings", help="Location of workflow settings to import from.")
    parser.add_argument("-r", "--relocate", action="store_true", help="Relocate the workflow directory to be relative to the import settings location.")


def _parse_args():
    parser = argparse.ArgumentParser(prog=info.APPLICATION_NAME)

    # Define subcommands
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: config maker
    config_maker_parser = subparsers.add_parser("config_maker", help="Create a configuration for importing into a workflow.")
    config_maker_parser.add_argument("-c", "--configuration", help="Configuration file location to write to.")
    config_maker_parser.add_argument("-d", "--definition", nargs=2, action='append',
                                     help="Definition to write into configuration, specified by 'step name:step identifier' and a key:value, can be used multiple times.")

    # Subcommand: user specified environment
    use_parser = subparsers.add_parser("use", help="Create a user specified environment.")
    use_parser.add_argument("-b", "--base_dir", help="Sets the base directory for the setup, the directory must exist.")
    use_parser.add_argument("-d", "--directory", action='append', help="Specify a plugin directory, can be used multiple times.")

    # Subcommand: headless
    headless_parser = subparsers.add_parser("headless", help="Run MAP Client in headless mode.")
    _common_workflow_args(headless_parser)

    _common_workflow_args(parser)

    return parser.parse_args(sys.argv[1:])


def main():
    args = _parse_args()

    if args.command == "config_maker":
        result = _config_maker_main(args.configuration, args.definition, False)
    elif args.command == "use":
        result = _user_specified_environment_main(args.base_dir, args.directory)
    elif args.command == "headless":
        result = sans_gui_main(args.workflow, args.import_settings, args.relocate)
    else:
        result = windows_main(args.workflow, args.execute)

    sys.exit(result)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
