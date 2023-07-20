from pkgutil import walk_packages

import mapclientplugins


# I don't think this will work if the plugin is zipped in an archive.
hiddenimports = ['mapclientplugins']
print("hook: mapclientplugins")
for module_loader, name, ispkg in walk_packages(mapclientplugins.__path__, 'mapclientplugins.'):
    hiddenimports.append(name)
    print("name:", name)
