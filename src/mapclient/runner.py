import argparse
import json
import os
import shutil
import sys

from mapclient.application import sans_gui_main
from mapclient.core.managers.workflowmanager import WorkflowManager
from mapclient.core.utils import is_json
from mapclient.settings.general import is_workflow, get_configuration_file

STEP_KNOWLEDGE_DATABASE = {
    "File Chooser": {
        "config_type": "json",
        "relative_path_keys": ["File", "previous_location"]
    },
    "Directory Copy": {
        "config_type": "json",
        "relative_path_keys": ["location", "previous_location"]
    },
}


def _parse_arguments():
    parser = argparse.ArgumentParser(prog="mapclient_workflow_runner")
    parser.add_argument("-w", "--workflow", required=True, help="Location of workflow to run")
    parser.add_argument("-c", "--configuration", required=True, help="Configuration information to apply to workflow")

    return parser.parse_args()


def _backup_file(file_path):
    return f"{file_path}.bak"


def _relative_path_keys_for_config(name):
    if name in STEP_KNOWLEDGE_DATABASE:
        return STEP_KNOWLEDGE_DATABASE[name].get("relative_path_keys", [])

    return None


def _backup_and_merge_config(location, config_file, config, config_name):
    errors = []
    config_type = _configuration_type_for(config_name)
    if config_type == "json":
        relative_path_keys = _relative_path_keys_for_config(config_name)
        if relative_path_keys is None:
            errors.append(f"Un-registered config relative path keys: '{config_name}'")
        else:
            shutil.copy2(config_file, _backup_file(config_file))
            with open(config_file) as fh:
                content = json.load(fh)

            for key in relative_path_keys:
                if key in config:
                    config[key] = os.path.relpath(config[key], location)

            content.update(config)
            with open(config_file, "w") as fh:
                json.dump(content, fh)
    else:
        errors.append(f"Config type for '{config_name}' is unknown.")

    return errors


def _restore_backup(config_file):
    os.rename(_backup_file(config_file), config_file)


def _configuration_type_for(name):
    return STEP_KNOWLEDGE_DATABASE.get(name, {"config_type": "not-set"})["config_type"]


def _determine_configuration_name(wf, identifier):
    name = "unknown"

    wf.beginGroup('nodes')
    nodeCount = wf.beginReadArray('nodelist')
    for i in range(nodeCount):
        wf.setArrayIndex(i)
        current_identifier = wf.value('identifier')
        if identifier == current_identifier:
            name = wf.value('name')
            break

    wf.endArray()
    wf.endGroup()

    return name


def workflow_runner(location, configuration):

    if not is_workflow(location):
        sys.exit(1)

    if not is_json(configuration):
        sys.exit(2)

    with open(configuration) as fh:
        config = json.load(fh)

    wf = WorkflowManager.load_workflow_virtually(location)

    errors = []
    modified_configs = []
    for identifier in config:
        config_file = get_configuration_file(location, identifier)
        if os.path.isfile(config_file):
            backup_errors = _backup_and_merge_config(location, config_file, config[identifier], _determine_configuration_name(wf, identifier))
            if backup_errors:
                errors.extend(backup_errors)
            else:
                modified_configs.append(config_file)
        else:
            errors.append(f"No corresponding configuration available for '{identifier}'.")

    if errors:
        for error in errors:
            print(error)
    else:
        sans_gui_main(location)

    for modified_config in modified_configs:
        _restore_backup(modified_config)


def main():
    args = _parse_arguments()
    workflow_runner(args.workflow, args.configuration)


if __name__ == "__main__":
    main()
