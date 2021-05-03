from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('mapclientplugins', include_py_files=True, excludes=['__pycache__'])
hiddenimports = ['imghdr']
