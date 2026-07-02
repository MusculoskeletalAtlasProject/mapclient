import json
import os

from PyInstaller.utils.hooks import collect_submodules

plugin_paths_file = os.path.join(os.getcwd(), 'mapclientplugins_paths.json')

print('plugin_paths_file:', plugin_paths_file)
print(os.path.isfile(plugin_paths_file))
print('done')
if os.path.isfile(plugin_paths_file):
    with open(plugin_paths_file) as f:
        plugin_paths = json.load(f)

    print('plugin_paths:', plugin_paths)
    hiddenimports = []
    for plugin_path, mode in plugin_paths:
        mapclientplugins_dir = os.path.join(plugin_path, 'mapclientplugins')
        if os.path.isdir(mapclientplugins_dir):
            for name in os.listdir(mapclientplugins_dir):
                if os.path.isdir(os.path.join(mapclientplugins_dir, name)) and not name.startswith('_'):
                    hiddenimports.append(f'mapclientplugins.{name}')
else:
    # Fallback for manual builds without the paths JSON; collects any installed mapclientplugins.
    hiddenimports = collect_submodules('mapclientplugins')
