import os
from tempfile import TemporaryDirectory
from zipfile import is_zipfile, ZipFile

from PySide6 import QtCore

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME


def import_settings(source_location):
    """
    Get the project information from the source location whether it is a
    Zip file or directory.

    :param source_location: A Zip file or directory.
    :return: A QtCore.QSettings object.
    """
    if is_zipfile(source_location):
        # Get project information for the imported workflow.
        with ZipFile(source_location) as archive:
            with TemporaryDirectory() as temp_dir:
                archive.extract(DEFAULT_WORKFLOW_PROJECT_FILENAME, temp_dir)
                import_proj = QtCore.QSettings(os.path.join(temp_dir, DEFAULT_WORKFLOW_PROJECT_FILENAME), QtCore.QSettings.Format.IniFormat)
    else:
        import_proj = QtCore.QSettings(source_location, QtCore.QSettings.Format.IniFormat)

    return import_proj
