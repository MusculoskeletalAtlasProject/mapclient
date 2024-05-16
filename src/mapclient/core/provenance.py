import json
import os
import pkgutil
import subprocess
import sys

from importlib import import_module

import dulwich.porcelain
from dulwich.repo import Repo

from mapclient.core.utils import is_frozen
from mapclient.settings.definitions import PLUGINS_PACKAGE_NAME, FROZEN_PROVENANCE_INFO_FILE


def _strip_pip_list_output(output_stream):
    output = {}
    content = output_stream.decode()
    lines = content.split('\n')
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        parts = line.split()
        if len(parts) > 1:
            output[parts[0]] = {'version': parts[1]}
            if len(parts) > 2:
                if parts[0] == 'mapclient' and os.path.isdir(parts[2]):
                    describe_result = describe_tag(parts[2])
                    describe_parts = describe_result.split('-')
                    if len(describe_parts) == 1 and describe_parts[0]:
                        location = remote_locations(os.path.dirname(parts[2]))
                    else:
                        location = f'local-repo-{describe_result}'

                    output[parts[0]]['location'] = location
                elif os.path.isdir(parts[2]):
                    output[parts[0]]['location'] = f'locally-acquired-{describe_tag(parts[2])}'
                else:
                    output[parts[0]]['location'] = parts[2]
            else:
                output[parts[0]]['location'] = 'PyPI'

    return output


def _determine_git_repo(src_dir, check_parent=True):
    git_repo = None
    if os.path.isdir(os.path.join(src_dir, ".git")):
        git_repo = src_dir
    elif check_parent and os.path.isdir(os.path.join(src_dir, "..", ".git")):
        git_repo = os.path.join(src_dir, "..")

    return git_repo


def _backup_get_remote_repo(r):
    config = r.get_config()
    remote_name = b'origin'
    remote_location = config.get((b'remote', remote_name), b"url")

    return remote_name.decode(), remote_location.decode()


def remote_locations(src_dir):
    git_repo = _determine_git_repo(src_dir, False)

    if git_repo is None:
        return "&&&&&&"

    with dulwich.porcelain.open_repo_closing(git_repo) as r:
        try:
            remote_repo_info = dulwich.porcelain.get_remote_repo(r)
        except IndexError:
            remote_repo_info = _backup_get_remote_repo(r)

    return remote_repo_info[1]


def describe_tag(src_dir, check_parent=True):
    git_repo = _determine_git_repo(src_dir, check_parent)

    if git_repo is None:
        return "******"

    r = Repo(git_repo)

    try:
        r.head()
    except KeyError:
        return "<no-commits-repo>"
    finally:
        r.close()

    return dulwich.porcelain.describe(git_repo)


def _determine_capabilities():
    try:
        import mapclientplugins
        mapclientplugins_present = True
    except ModuleNotFoundError:
        mapclientplugins_present = False

    my_env = os.environ.copy()
    python_executable = sys.executable

    result = subprocess.run([python_executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)

    package_info = _strip_pip_list_output(result.stdout)

    plugin_names = []
    mapclient_plugins_info = {}
    if mapclientplugins_present:
        for loader, module_name, is_pkg in pkgutil.walk_packages(mapclientplugins.__path__):
            if is_pkg:
                package_name = PLUGINS_PACKAGE_NAME + '.' + module_name
                try:
                    plugin_names.append(package_name)
                    module = import_module(package_name)
                    mapclient_plugins_info[package_name] = {
                        "version": module.__version__ if hasattr(module, '__version__') else "X.Y.Z",
                        "location": module.__location__ if hasattr(module, '__location__') else "<plugin-location-not-set>",
                    }
                except ModuleNotFoundError:
                    pass
                except ImportError:
                    pass

    mapclient_info = {'version': 'unknown', 'location': 'unknown'}
    if 'mapclient' in package_info:
        mapclient_info = package_info['mapclient']

    for key in ['mapclient'] + plugin_names:
        if key in package_info:
            del package_info[key]

    return {'version': '0.1.0', 'id': 'map-client-provenance-record', 'mapclient': mapclient_info, 'plugins': mapclient_plugins_info, 'packages': package_info}


def reproducibility_info():
    if is_frozen():
        info_file = os.path.join(sys._MEIPASS, FROZEN_PROVENANCE_INFO_FILE)
        with open(info_file) as f:
            content = f.read()
        r = json.loads(content)
    else:
        r = _determine_capabilities()

    return r
