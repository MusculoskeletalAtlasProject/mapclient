import argparse
import json

from mapclient.core.utils import is_json


def _parse_arguments():
    parser = argparse.ArgumentParser(prog="mapclient_config_maker")
    parser.add_argument("-c", "--configuration", required=True, help="Configuration file location to write to")
    parser.add_argument("-d", "--definition", nargs=2, action='append', help="Definition to write into configuration, specified by identifier key:value")
    parser.add_argument("-a", "--append", action="store_true", help="Append/merge definitions don't overwrite entire configuration file")

    return parser.parse_args()


def _split_key_value_definition(text):
    index = text.find(":")
    return text[:index], text[index + 1:]


def config_maker(configuration_file, definitions, append):
    existing_configuration = is_json(configuration_file)
    content = {}
    if existing_configuration and append:
        with open(configuration_file) as fh:
            content = json.load(fh)

    for definition in definitions:
        identifier = definition[0]
        key, value = _split_key_value_definition(definition[1])
        identifier_data = content.get(identifier, {})
        identifier_data[key] = value
        content[identifier] = identifier_data

    with open(configuration_file, "w") as fh:
        json.dump(content, fh)


def main():
    args = _parse_arguments()
    config_maker(args.configuration, args.definition, args.append)


if __name__ == "__main__":
    main()
