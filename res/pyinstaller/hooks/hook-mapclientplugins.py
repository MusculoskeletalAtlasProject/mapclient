from PyInstaller.utils.hooks import collect_submodules


# I don't think this will work if the plugin is zipped in an archive.
hiddenimports = collect_submodules('mapclientplugins')
