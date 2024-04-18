import os
import json
from packaging import version

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QStyle, QStyleOptionButton, QInputDialog, QLineEdit, QMessageBox, QTreeView

from mapclient.core.workflow.workflowsteps import addStep
from mapclient.view.workflow.workflowsteptreeview import HeaderDelegate, WorkflowStepTreeView
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
setattr(MAPPlugin, 'getCategory', MAPPlugin.get_category)
setattr(MAPPlugin, 'getIcon', lambda self: None)


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
    buttonClicked = QtCore.Signal(str, str)

    def __init__(self, parent=None, installed_versions=None, database_versions=None):
        super().__init__(parent)
        self._pressed = None
        self._installed_versions = installed_versions
        self._database_versions = database_versions
        self._download_icon = QtGui.QPixmap(':/mapclient/images/download_icon.png')
        self._downloaded_icon = QtGui.QPixmap(':/mapclient/images/downloaded_icon.png')
        self._loading_icon = QtGui.QPixmap(':/mapclient/images/loading_icon.png')

    def get_installed_versions(self):
        return self._installed_versions

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
                painter.drawText(_get_label_pos(option), QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight, installed_version)
            else:
                opt.icon = self._download_icon

            opt.iconSize = QtCore.QSize(48, 48)
            opt.rect = _get_button_rect(option.rect)

            if self._pressed and self._pressed == (index.row(), index.column()):
                opt.state = QStyle.State_Enabled | QStyle.State_Sunken
            else:
                opt.state = QStyle.State_Enabled | QStyle.State_Raised
            QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter)

    def editorEvent(self, event, model, option, index):
        if index.parent().row() < 0:
            return False

        name = index.data()
        if (name in self._installed_versions.keys()) and self._installed_versions[name] >= self._database_versions[name]:
            return True

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if _get_button_rect(option.rect).contains(event.pos()):
                self._pressed = (index.row(), index.column())
            return True

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._pressed == (index.row(), index.column()):
                if _get_button_rect(option.rect).contains(event.pos()):
                    plugin = model.data(index, QtCore.Qt.UserRole + 1)
                    self.buttonClicked.emit(name, plugin.get_url())
            self._pressed = None
            return True

        return False


def _get_button_rect(option_rect):
    button_rect = QtCore.QRect()
    button_rect.setRect(option_rect.width() - 58, option_rect.y() + 8, 48, 48)
    return button_rect


def _get_label_pos(option):
    label_rect = QtCore.QRect(option.rect.x(), option.rect.y(), option.rect.width() - 70, option.rect.height())
    return label_rect


class PluginTreeView(WorkflowStepTreeView):
    selection_changed = QtCore.Signal(list)

    def mousePressEvent(self, event):
        QTreeView.mousePressEvent(self, event)
        item = self.indexAt(event.pos())

        if not item.parent().row() < 0:
            item_rect = self.visualRect(item)
            if not _get_button_rect(item_rect).contains(event.pos()):
                self.selectionModel().select(item, QtCore.QItemSelectionModel.Toggle)
                self.selection_changed.emit(self.selectionModel().selectedIndexes())


def _authenticate_github_user():
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
    cached_database, cached_timestamp = _get_cached_database()
    remote_timestamp = _get_remote_database_timestamp()

    if not remote_timestamp:
        print("Retrieving remote database failed. Using cached database.")
        return cached_database

    if cached_timestamp < remote_timestamp:
        data = _cache_plugin_database()
        if data:
            cached_database = data

    return cached_database


def _get_cache_file_path():
    return os.path.join(get_data_directory(), "plugin_database.json")


def _get_cached_database():
    database_file = _get_cache_file_path()
    try:
        with open(database_file, "r") as file:
            cached_database = json.load(file, object_hook=from_json)
        cached_timestamp = os.path.getmtime(database_file)

        return cached_database, cached_timestamp
    except IOError:
        return {}, 0.0


def _cache_plugin_database():
    database = _get_remote_database()

    database_file = _get_cache_file_path()
    if not os.path.exists(os.path.dirname(database_file)):
        os.mkdir(os.path.dirname(database_file))

    with open(database_file, "w") as file:
        json.dump(database, file, default=default)

    return database


def _get_remote_database():
    return _github_api_wrapper(lambda r: json.loads(r.get_contents("plugin_database.json").decoded_content.decode(), object_hook=from_json))


def _get_remote_database_timestamp():
    return _github_api_wrapper(lambda r: r.updated_at.timestamp())


def _github_api_wrapper(f):
    def call_inner():
        repo = g.get_repo("MusculoskeletalAtlasProject/map-plugin-database")
        return f(repo)

    try:
        g = Github()
        return call_inner()
    except RateLimitExceededException:
        g = _authenticate_github_user()
        if not g:
            return None
        return call_inner()


def from_json(json_dict):
    if '_name' in json_dict.keys():
        return MAPPlugin.from_json(json_dict)
    else:
        return json_dict


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
