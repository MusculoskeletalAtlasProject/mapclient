import os
import pkgutil
import subprocess
import sys
from importlib import import_module

from mapclient.core.utils import is_frozen
from mapclient.settings import info
from mapclient.settings.definitions import PLUGINS_PACKAGE_NAME


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
                output[parts[0]]['location'] = parts[2]

    return output


def _determine_capabilities():
    my_env = os.environ.copy()
    python_executable = sys.executable

    result = subprocess.run([python_executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)

    output_info = _strip_pip_list_output(result.stdout)
    import mapclientplugins
    # print(pkgutil.walk_packages(mapclientplugins.__path__))
    mapclientplugins_info = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(mapclientplugins.__path__):
        if is_pkg:
            package_name = PLUGINS_PACKAGE_NAME + '.' + module_name
            module = import_module(package_name)
            mapclientplugins_info[package_name] = {
                "version": module.__version__ if hasattr(module, '__version__') else "X.Y.Z",
                "location": module.__location__ if hasattr(module, '__location__') else "",
            }

    return {'mapclient': info.VERSION_STRING, **output_info, **mapclientplugins_info}


def reproducibility_info():
    if is_frozen():
        print('Getting hard-coded information.')
        r = {}
    else:
        r = _determine_capabilities()

    return r
