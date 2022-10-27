import os
import json

from PySide2 import QtGui

from mapclient.core.workflow.workflowsteps import addStep


class MAPPlugin:
    def __init__(self, name, category, icon_name, url):
        """
        This is a simplified version of the WorkflowSteps class, to be used for visualizing step objects that aren't installed locally.
        """
        self._name = name
        self._category = category
        self._icon = icon_name
        self._url = url

    def get_name(self):
        return self._name

    def get_category(self):
        return self._category

    def get_icon_name(self):
        return self._icon

    def get_url(self):
        return self._url

    def __iter__(self):
        yield from {
            "_name": self._name,
            "_category": self._category,
            "_icon": self._icon,
            "_url": self._url
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dict):
        return MAPPlugin(json_dict['_name'], json_dict['_category'], json_dict['_icon'], json_dict['_url'])


# This makes the MAPPlugin class compatible with workflowsteps.addStep().
setattr(MAPPlugin, 'getName', MAPPlugin.get_name)


class PluginData(QtGui.QStandardItemModel):

    def __init__(self, timestamp, plugins, parent=None):
        super(PluginData, self).__init__(parent)
        self._timestamp = float(timestamp)
        self._plugins = plugins

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def get_plugins(self):
        return self._plugins

    def reload(self):
        self.clear()
        self.setColumnCount(1)
        for plugin in self._plugins.values():
            addStep(self, plugin)

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        _plugins = {}
        for key, plugin in self._plugins.items():
            _plugins[key] = plugin.__dict__

        return {"_timestamp": self._timestamp, "_plugins": _plugins}

    @staticmethod
    def from_json(json_dict):
        if '_name' in json_dict.keys():
            return MAPPlugin.from_json(json_dict)
        elif '_plugins' in json_dict.keys():
            return PluginData(json_dict['_timestamp'], json_dict['_plugins'])
        else:
            return json_dict


def get_step_database_file():
    return os.path.join(os.path.dirname(__file__), 'plugin_manager', 'plugin_database.json')


def read_step_database():
    database_file = get_step_database_file()

    try:
        with open(database_file, "r") as file:
            data = json.loads(file.read(), object_hook=PluginData.from_json)
    except IOError:
        data = PluginData(0.0, {})

    return data


def write_step_database(data):
    database_file = get_step_database_file()
    if not os.path.exists(os.path.dirname(database_file)):
        os.mkdir(os.path.dirname(database_file))

    with open(database_file, "w") as file:
        file.write(json.dumps(data, default=default))


def read_step_info(step_file):
    category = icon_path = None
    lines = step_file.splitlines()
    for line in lines:
        line = line.strip()

        if line.startswith("self._category"):
            category = line[line.find("=") + 1:].strip(' "\'\t\r\n')
            if icon_path:
                break
        elif line.startswith("self._icon"):
            icon_path = line[line.find("(") + 2: line.rfind(")") - 1].strip()
            if category:
                break

    return category, icon_path


def get_icon(plugin):
    icon_path = os.path.join(os.path.dirname(__file__), 'plugin_manager', 'icons', plugin['icon_name'])

    return QtGui.QImage(icon_path)


def save_plugin_icon(icon_path):
    save_dir = os.path.join(os.path.dirname(__file__), 'plugin_manager', 'icons')

    # TODO: Implement.
    icon_name = ""

    return icon_name


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
