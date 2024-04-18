import argparse
import json
import os
import platform

import PySide2 as RefMod

import PyInstaller.__main__

from mapclient.core.provenance import reproducibility_info
from mapclient.settings.definitions import FROZEN_PROVENANCE_INFO_FILE


# Set Python optimisations on.
os.environ['PYTHONOPTIMIZE'] = '1'

here = os.path.dirname(__file__)


def main(variant):
    run_command = [
        '../../src/mapclient/application.py',
        '-n', f'MAP-Client{variant}',
        # '--debug', 'noarchive',
        '--windowed',
        '--no-embed-manifest',
        '--noconfirm',
        '--hidden-import', 'scipy',
        '--hidden-import', 'scipy.interpolate',
        '--hidden-import', 'numpy',
        '--hidden-import', 'mapclientplugins',
        # '--hidden-import', 'opencmiss.utils',
        # '--hidden-import', 'opencmiss.zincwidgets',
        '--hidden-import', 'opencmiss.zinc',
        '--additional-hooks-dir=hooks',
    ]

    info = reproducibility_info()
    info_file = FROZEN_PROVENANCE_INFO_FILE
    with open(info_file, 'w') as f:
        f.write(json.dumps(info, default=lambda o: o.__dict__, sort_keys=True, indent=2))

    data = os.pathsep.join([info_file, '.'])
    run_command.append(f'--add-data={data}')

    images_dir = os.path.join('..', '..', 'src', 'mapclient', 'tools', 'pluginwizard', 'qt', 'images')
    names = os.listdir(images_dir)
    for name in names:
        data = os.pathsep.join([os.path.join(os.path.abspath(images_dir), name), os.path.join('res', 'images')])
        run_command.append(f'--add-data={data}')

    pyside_dir = os.path.dirname(RefMod.__file__)

    if platform.system() == 'Darwin':
        rcc_exe = os.path.join(pyside_dir, "rcc")
        uic_exe = os.path.join(pyside_dir, "uic")

        macos_icon = os.path.join('..', 'macos', 'MAP-Client.icns')
        run_command.append(f'--icon={macos_icon}')

    elif platform.system() == "Windows":
        rcc_exe = os.path.join(pyside_dir, "rcc.exe")
        uic_exe = os.path.join(pyside_dir, "uic.exe")

        win_icon = os.path.join(here, '..', 'win', 'MAP-Client.ico')
        run_command.append(f'--icon={win_icon}')
    else:
        raise NotImplementedError("Platform is not supported for creating a MAP Client application.")

    run_command.append(os.pathsep.join([f'--add-binary={rcc_exe}', 'PySide2/']))
    run_command.append(os.pathsep.join([f'--add-binary={uic_exe}', 'PySide2/']))

    externally_specified_internal_workflows_zip = os.environ.get('INTERNAL_WORKFLOWS_ZIP', '<not-a-file>')
    if os.path.isfile(externally_specified_internal_workflows_zip):
        internal_workflows_zip = externally_specified_internal_workflows_zip
    else:
        internal_workflows_zip = os.path.abspath(os.path.join('..', '..', 'src', 'internal_workflows.zip'))

    if os.path.isfile(internal_workflows_zip):
        data = os.pathsep.join([internal_workflows_zip, '.'])
        run_command.append(f'--add-data={data}')

    print('Running command: ', run_command)
    PyInstaller.__main__.run(run_command)

    os.remove(info_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="create_installer")
    parser.add_argument("variant", nargs='?', default='', help="MAP Client variant")
    args = parser.parse_args()

    app_variant = ''
    if args.variant:
        app_variant = f"-{args.variant}"

    main(app_variant)
