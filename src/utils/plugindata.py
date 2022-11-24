import os
import json
from packaging import version

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QStyle, QStyleOptionButton, QInputDialog, QLineEdit, QMessageBox

from mapclient.core.workflow.workflowsteps import addStep
from mapclient.view.workflow.workflowsteptreeview import HeaderDelegate
from mapclient.settings.general import get_data_directory

from github import Github
from github.GithubException import BadCredentialsException, RateLimitExceededException


class MAPPlugin:
    def __init__(self, name, category, icon_name, url, version_number):
        """
        This is a simplified version of the WorkflowSteps class, to be used for visualizing step objects that aren't installed locally.
        """
        self._name = name
        self._category = category
        self._icon = icon_name
        self._url = url
        self._version = version_number

    def get_name(self):
        return self._name

    def get_category(self):
        return self._category

    def get_icon_name(self):
        return self._icon

    def get_url(self):
        return self._url

    def get_version(self):
        return self._version

    def __iter__(self):
        yield from {
            "_name": self._name,
            "_category": self._category,
            "_icon": self._icon,
            "_url": self._url,
            "_version": self._version
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dict):
        return MAPPlugin(json_dict['_name'], json_dict['_category'], json_dict['_icon'], json_dict['_url'], json_dict['_version'])


# This makes the MAPPlugin class compatible with workflowsteps.addStep().
setattr(MAPPlugin, 'getName', MAPPlugin.get_name)


class PluginData(QtGui.QStandardItemModel):

    def __init__(self, plugins, parent=None):
        super(PluginData, self).__init__(parent)
        self._plugins = plugins

    def reload(self):
        self.clear()
        self.setColumnCount(1)
        for plugin in self._plugins.values():
            addStep(self, plugin)


class PushButtonDelegate(HeaderDelegate):
    buttonClicked = QtCore.Signal(str)

    def __init__(self, parent=None, installed_versions=None, database_versions=None):
        super().__init__(parent)
        self._pressed = None
        self._installed_versions = installed_versions
        self._database_versions = database_versions
        self._download_icon = QtGui.QPixmap(':/mapclient/images/download_icon.png')
        self._downloaded_icon = QtGui.QPixmap(':/mapclient/images/downloaded_icon.png')
        self._loading_icon = QtGui.QPixmap(':/mapclient/images/loading_icon.png')

    def paint(self, painter, option, index):
        super(PushButtonDelegate, self).paint(painter, option, index)

        if not index.parent().row() < 0:
            opt = QStyleOptionButton()

            name = index.data()
            if name in self._installed_versions.keys():
                installed_version = self._installed_versions[name]
                if version.parse(self._database_versions[name]) > version.parse(installed_version):
                    installed_version += " ▼"
                    opt.icon = self._download_icon
                elif self._installed_versions[name]:
                    opt.icon = self._downloaded_icon
                else:
                    opt.icon = self._loading_icon
                painter.drawText(self.get_label_pos(option), QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight, installed_version)
            else:
                opt.icon = self._download_icon

            opt.iconSize = QtCore.QSize(48, 48)
            opt.rect = self.get_button_rect(option)

            if self._pressed and self._pressed == (index.row(), index.column()):
                opt.state = QStyle.State_Enabled | QStyle.State_Sunken
            else:
                opt.state = QStyle.State_Enabled | QStyle.State_Raised
            QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter)

    def editorEvent(self, event, model, option, index):
        name = index.data()
        if (name in self._installed_versions.keys()) and self._installed_versions[name] >= self._database_versions[name]:
            return True

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if self.get_button_rect(option).contains(event.pos()):
                self._pressed = (index.row(), index.column())
            return True

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._pressed == (index.row(), index.column()):
                if self.get_button_rect(option).contains(event.pos()):
                    plugin = model.data(index, QtCore.Qt.UserRole + 1)
                    self.buttonClicked.emit(plugin.get_url())
            self._pressed = None
            return True

        return False

    @staticmethod
    def get_button_rect(option):
        button_rect = QtCore.QRect()
        button_rect.setRect(option.rect.width() - 58, option.rect.y() + 8, 48, 48)
        return button_rect

    @staticmethod
    def get_label_pos(option):
        label_rect = QtCore.QRect(option.rect.x(), option.rect.y(), option.rect.width() - 70, option.rect.height())
        return label_rect


def authenticate_github_user():
    print("GitHub API rate limit exceeded. GitHub personal access token required.")
    try:
        token = os.environ["GITHUB_PAT"]
        g = Github(token)
        _ = g.get_user().name
        return g
    except (KeyError, BadCredentialsException):
        if QApplication.instance() is None:
            _ = QApplication([])
        while True:
            try:
                token, ok = QInputDialog().getText(None, "GitHub PAT", "GITHUB_PAT cannot be found or is invalid. "
                                                   "Please provide a Personal Access Token for GitHub:", QLineEdit.Password)
                if ok:
                    g = Github(token)
                    _ = g.get_user().name
                    os.environ["GITHUB_PAT"] = token
                    return g
                else:
                    return None
            except BadCredentialsException:
                QMessageBox.information(None, 'Token Invalid', 'The Personal Access Token given is not valid.')


# This method is used by the visualisation script to get an up-to-date version of the plugin database. DB in dictionary format.
def get_plugin_database():
    cached_database, cached_timestamp = get_cached_database()
    remote_timestamp = get_remote_database_timestamp()

    if not remote_timestamp:
        print("Retrieving remote database failed. Using cached database.")
        return cached_database

    if cached_timestamp < remote_timestamp:
        data = cache_plugin_database()
        if data:
            cached_database = data

    return cached_database


def get_cache_file_path():
    return os.path.join(get_data_directory(), "plugin_database.json")


def get_cached_database():
    database_file = get_cache_file_path()
    try:
        with open(database_file, "r") as file:
            cached_database = json.load(file, object_hook=from_json)
        cached_timestamp = os.path.getmtime(database_file)

        return cached_database, cached_timestamp
    except IOError:
        return {}, 0.0


def cache_plugin_database():
    database = get_remote_database()

    database_file = get_cache_file_path()
    if not os.path.exists(os.path.dirname(database_file)):
        os.mkdir(os.path.dirname(database_file))

    with open(database_file, "w") as file:
        json.dump(database, file, default=default)

    return database


def get_remote_database():
    return github_api_wrapper(lambda r: json.loads(r.get_contents("plugin_database.json").decoded_content.decode(), object_hook=from_json))


def get_remote_database_timestamp():
    return github_api_wrapper(lambda r: r.updated_at.timestamp())


def get_plugin_sources():
    return github_api_wrapper(lambda r: json.loads(r.get_contents("plugin_sources.json").decoded_content.decode()))


def github_api_wrapper(f):
    def call_inner():
        repo = g.get_repo("MusculoskeletalAtlasProject/map-plugin-database")
        return f(repo)

    try:
        g = Github()
        return call_inner()
    except RateLimitExceededException:
        g = authenticate_github_user()
        if not g:
            return None
        return call_inner()


def from_json(json_dict):
    if '_name' in json_dict.keys():
        return MAPPlugin.from_json(json_dict)
    else:
        return json_dict


def write_step_database(data):
    pass


def read_step_info(step_file):
    def read_value(identifier):
        value = read_line(line, identifier)
        if not value:
            extended_line = line + next(lines).strip(' \t\r\n')
            value = read_line(extended_line, identifier)

        return value

    name = category = icon_path = None
    lines = iter(step_file.splitlines())
    for line in lines:
        line = line.strip()

        if line.startswith("super"):
            name = read_value("__init__")
        elif line.startswith("self._category"):
            category = read_value("=")
            if icon_path:
                break
        elif line.startswith("self._icon"):
            icon_path = read_value("QImage")
            if category:
                break

    return name, category, icon_path


def read_line(line, identifier):

    value = None
    for quote in ["'", '"']:
        start = line.find(quote, line.find(identifier) + len(identifier))
        if start == -1:
            continue
        end = line.find(quote, start + 1)
        value = line[start:end].strip(' "\'\t\r\n')

    return value


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
