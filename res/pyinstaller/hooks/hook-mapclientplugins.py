import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, get_package_paths

import mapclientplugins

print("==================================")
print(mapclientplugins.__path__)
# hidden = []
# for p in mapclientplugins.__path__:
#     d = os.path.dirname(p)
# print(collect_submodules('mapclientplugins'))
# print(get_package_paths('mapclientplugins'))
# print(collect_data_files('mapclientplugins', include_py_files=True, excludes=['__pycache__']))
print("==================================")
datas = collect_data_files('mapclientplugins', include_py_files=True, excludes=['__pycache__'])
# hiddenimports = ['imghdr', 'mapclientplugins', 'mapclientplugins.datatrimmerstep']
# hiddenimports = (['mapclientplugins'])
