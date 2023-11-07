import json
import os
import pkgutil
import subprocess
import sys

from importlib import import_module

import dulwich.porcelain

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
                    output[parts[0]]['location'] = _describe_tag(parts[2])
                elif os.path.isdir(parts[2]):
                    output[parts[0]]['location'] = f'locally-acquired-{_describe_tag(parts[2])}'
                else:
                    output[parts[0]]['location'] = parts[2]
            else:
                output[parts[0]]['location'] = 'pypi'

    return output


def _describe_tag(src_dir):
    git_repo = None
    if os.path.isdir(os.path.join(src_dir, ".git")):
        git_repo = src_dir
    elif os.path.isdir(os.path.join(src_dir, "..", ".git")):
        git_repo = os.path.join(src_dir, "..")

    if git_repo is None:
        return "******"

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

    mapclientplugins_info = {}
    if mapclientplugins_present:
        for loader, module_name, is_pkg in pkgutil.walk_packages(mapclientplugins.__path__):
            if is_pkg:
                package_name = PLUGINS_PACKAGE_NAME + '.' + module_name
                try:
                    module = import_module(package_name)
                    mapclientplugins_info[package_name] = {
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
        del package_info['mapclient']

    return {'mapclient': mapclient_info, 'plugins': mapclientplugins_info, 'packages': package_info}


def reproducibility_info():
    if is_frozen():
        info_file = os.path.join(sys._MEIPASS, FROZEN_PROVENANCE_INFO_FILE)
        with open(info_file) as f:
            content = f.read()
        r = json.loads(content)
    else:
        r = _determine_capabilities()

    return r
