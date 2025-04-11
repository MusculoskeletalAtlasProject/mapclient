import argparse
import os.path
import sys
from zipfile import is_zipfile, ZipFile

from PySide6 import QtWidgets

from mapclient.application import prepare_sans_gui_app
from mapclient.core.managers.workflowmanager import WorkflowManager
from mapclient.core.workflow.workflowscene import create_from
from mapclient.settings.general import get_configuration_file


def _parse_arguments():
    parser = argparse.ArgumentParser(prog="mapclient_config_maker")
    parser.add_argument("-c", "--configuration", required=True, help="Configuration file location to write to")
    parser.add_argument("-d", "--definition", nargs=2, action='append', help="Definition to write into configuration, specified by identifier key:value")
    parser.add_argument("-a", "--append", action="store_true", help="Append/merge definitions don't overwrite entire configuration file")

    return parser.parse_args()


def _split_key_value_definition(text):
    index = text.find(":")
    if index == -1:
        return text, ""
    return text[:index], text[index + 1:]


def config_maker(configuration_file, definitions, append):
    is_file = os.path.isfile(configuration_file)
    is_zip = is_zipfile(configuration_file)
    if is_file and not is_zip:
        return 1

    if definitions is None:
        return 2

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

    app = QtWidgets.QApplication()
    model = prepare_sans_gui_app(app)
    pm = model.pluginManager()
    pm.load()

    files_created = []

    wf = WorkflowManager.create_empty_workflow(location)
    steps = create_from(wf, required_steps, None, location)
    files_created.append(wf.fileName())
    del wf

    for index, step in enumerate(steps):
        step_configurations = workflow_settings[step.getName()]
        step_configuration = step_configurations[step.getIdentifier()]
        step.setConfiguration(step_configuration)
        current_config_file = get_configuration_file(location, step.getIdentifier())
        with open(current_config_file, "w") as fh:
            fh.write(step.serialize())

        files_created.append(current_config_file)

    zip_file = os.path.join(location, "workflow-settings.zip")

    with ZipFile(zip_file, "w") as fh:
        for f in files_created:
            archive_name = os.path.relpath(f, location)
            fh.write(f, arcname=archive_name)
            os.remove(f)

    return 0


def main():
    args = _parse_arguments()
    return config_maker(args.configuration, args.definition, args.append)


if __name__ == "__main__":
    sys.exit(main())
