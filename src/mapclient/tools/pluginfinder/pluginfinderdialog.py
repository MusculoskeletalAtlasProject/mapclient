"""
This tool is used to search for new MAP Client plugins.

Author: Timothy Salemink
"""

import os
import time
import json
import logging

from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QDialog

from github import Github
from github.GithubException import UnknownObjectException

from mapclient.core.workflow.workflowsteps import WorkflowStepsFilter, addStep

from mapclient.settings.general import get_data_directory
from mapclient.tools.pluginfinder.ui.ui_pluginfinderdialog import Ui_PluginFinderDialog

logger = logging.getLogger(__name__)


class PluginFinderDialog(QDialog):
    """
    Manages information for finding and installing new MAP Client plugins.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_PluginFinderDialog()
        self._ui.setupUi(self)

        # Time in seconds between automatic update checks.
        self._refresh_timer = 3600.0
        # The following variables define where the Plugin Finder searches for plugin repositories.
        self._plugin_organisations = ['mapclient-plugins']
        self._plugin_repositories = []

        self._plugins_outdated = False
        self._plugin_data = read_step_database()
        self._filtered_plugins = WorkflowStepsFilter()
        self._filtered_plugins.setSourceModel(self._plugin_data)
        self._ui.stepTreeView.setModel(self._filtered_plugins)
        self.update_available_steps()
        self.expand_step_tree()

        self._make_connections()

        self._check_database()

    def _make_connections(self):
        self._ui.lineEditFilter.textChanged.connect(self._filter_text_changed)

    def _filter_text_changed(self, text):
        reg_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
        self._ui.stepTreeView.setFilterRegExp(reg_exp)

    def update_available_steps(self):
        self._plugin_data.reload()
        self._filtered_plugins.sort(QtCore.Qt.AscendingOrder)

    def expand_step_tree(self):
        self._ui.stepTreeView.expandAll()

    def _check_database(self):
        timestamp = self._plugin_data.get_timestamp()
        current_time = time.time()
        if (timestamp + self._refresh_timer) < current_time:
            self._check_plugins_for_updates()
            self._plugin_data.set_timestamp(current_time)
            write_step_database(self._plugin_data)

    def _check_plugins_for_updates(self):
        def check_plugin_info():
            name = repo.name
            updated_at = repo.updated_at.timestamp()
            if (name not in self._plugin_data.get_plugins().keys()) or (self._plugin_data.get_plugins()[name].get_timestamp() < updated_at):
                try:
                    step_file = repo.get_contents(f'mapclientplugins/{name}/step.py').decoded_content.decode()
                    category, icon_path = _read_step_info(step_file)
                    icon_name = _save_plugin_icon(icon_path)
                    self._plugin_data.get_plugins()[name] = MAPPlugin(name, updated_at, category, icon_name)
                    self._plugins_outdated = True
                except UnknownObjectException:
                    print(f"GitHub repository \"{repo.full_name}\" in not a valid MAP-Client plugin.")

        def _save_plugin_icon(icon_path):
            save_dir = os.path.join(get_data_directory(), 'plugin_manager', 'icons')

            # TODO: Implement.
            icon_name = ""

            return icon_name

        g = Github()
        self._plugins_outdated = False
        for organisation in self._plugin_organisations:
            org = g.get_organization(organisation)
            for repo in org.get_repos():
                check_plugin_info()

        for repository in self._plugin_repositories:
            repo = g.get_repo(repository)
            check_plugin_info()

        if self._plugins_outdated:
            self.update_available_steps()
            self.expand_step_tree()


def get_step_database_file():
    return os.path.join(get_data_directory(), 'plugin_manager', 'plugin_database.json')


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


def _read_step_info(step_file):
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
    icon_path = os.path.join(get_data_directory(), 'plugin_manager', 'icons', plugin['icon_name'])

    return QtGui.QImage(icon_path)


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


class MAPPlugin:

    def __init__(self, name, timestamp, category, icon_name):
        self._name = name
        self._timestamp = timestamp
        self._category = category
        self._icon = icon_name

    def get_name(self):
        return self._name

    def get_timestamp(self):
        return self._timestamp

    def get_category(self):
        return self._category

    def get_icon_name(self):
        return self._icon

    def __iter__(self):
        yield from {
            "_name": self._name,
            "_timestamp": self._timestamp,
            "_category": self._category,
            "_icon": self._icon
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dict):
        return MAPPlugin(json_dict['_name'], json_dict['_timestamp'], json_dict['_category'], json_dict['_icon'])


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
