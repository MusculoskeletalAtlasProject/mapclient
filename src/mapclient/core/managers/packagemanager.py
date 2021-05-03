import sys


"""
Class for managing external packages.

Adding package directories to the Python search path.
"""
class PackageManager(object):

    def __init__(self):
        self._directories = []
        self._modified = False

    def directories(self):
        return self._directories

    def set_directories(self, directories):
        if self._directories != directories:
            self._modified = True
        self._directories = directories

    def is_modified(self):
        return self._modified

    def load(self):
        modified = False
        for directory in self._directories:
            if directory not in sys.path:
                sys.path.append(directory)
                modified = True

        self._modified = False
        return modified

    def read_settings(self, settings):
        self._directories = []
        settings.beginGroup('Packages')
        directory_count = settings.beginReadArray('directories')
        for i in range(directory_count):
            settings.setArrayIndex(i)
            self._directories.append(settings.value('directory'))
        settings.endArray()
        settings.endGroup()

    def write_settings(self, settings):
        settings.beginGroup('Packages')
        settings.beginWriteArray('directories')
        directory_index = 0
        for directory in self._directories:
            settings.setArrayIndex(directory_index)
            settings.setValue('directory', directory)
            directory_index += 1
        settings.endArray()
        settings.endGroup()
