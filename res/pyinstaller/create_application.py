import argparse
import glob
import json
import os
import platform
import site

import PySide6 as RefMod

import PyInstaller.__main__

from mapclient.core.provenance import reproducibility_info
from mapclient.settings.definitions import APPLICATION_NAME, FROZEN_PROVENANCE_INFO_FILE


# Set Python optimisations on.
os.environ['PYTHONOPTIMIZE'] = '1'

here = os.path.dirname(__file__)

NS_IMPORT_INFRASTRUCTURE = """
import sys, types, os;p = os.path.join('{plugin_path}', *('mapclientplugins',));importlib = __import__('importlib.util');__import__('importlib.machinery');m = sys.modules.setdefault('mapclientplugins', importlib.util.module_from_spec(importlib.machinery.PathFinder.find_spec('mapclientplugins', [os.path.dirname(p)])));m = m or sys.modules.setdefault('mapclientplugins', types.ModuleType('mapclientplugins'));mp = (m or []) and m.__dict__.setdefault('__path__',[]);(p not in mp) and mp.append(p)
"""

def _create_plugin_ns_pth_file(plugin_dir, site_packages_dir):
    dir_name = os.path.basename(plugin_dir).replace('.', '_')
    existing_pth_file = os.path.join(plugin_dir, f'{dir_name}*-nspkg.pth')
    matching_files = glob.glob(existing_pth_file)
    if not matching_files:
        pth_file = os.path.join(site_packages_dir, f'{dir_name}-nspkg.pth')
        with open(pth_file, 'w') as fh:
            fh.write(NS_IMPORT_INFRASTRUCTURE.format(plugin_path=plugin_dir))


def _create_egg_info_directory(plugin_dir):
    listing = os.listdir(os.path.join(plugin_dir, 'mapclientplugins'))
    for item in listing:
        if os.path.isdir(os.path.join(plugin_dir, 'mapclientplugins', item)):
            if os.path.isfile(os.path.join(plugin_dir, 'mapclientplugins', item, '__init__.py')):
                egg_info_dir_name = f'mapclientplugins.{item}.egg-info'
                os.makedirs(os.path.join(plugin_dir, egg_info_dir_name), exist_ok=True)
                with open(os.path.join(plugin_dir, egg_info_dir_name, 'namespace_packages.txt'), 'w') as fh:
                    fh.write('mapclientplugins\n')


def main(variant):
    run_command = [
        '../../src/mapclient/application.py',
        '-n', f'{APPLICATION_NAME}{variant}',
        # '--debug', 'noarchive',
        '--windowed',
        # '--console',
        '--noconfirm',
        '--hidden-import', 'scipy',
        '--hidden-import', 'scipy.interpolate',
        '--hidden-import', 'numpy',
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

    pyside_resource_tool_dir = ['PySide6']
    if platform.system() == 'Darwin':
        rcc_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "rcc")
        uic_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "uic")

        pyside_resource_tool_dir.extend(['Qt', 'libexec'])

        macos_icon = os.path.join('..', 'macos', 'MAP-Client.icns')
        run_command.append(f'--icon={macos_icon}')

    elif platform.system() == "Windows":
        rcc_exe = os.path.join(pyside_dir, "rcc.exe")
        uic_exe = os.path.join(pyside_dir, "uic.exe")

        win_icon = os.path.join(here, '..', 'win', 'MAP-Client.ico')
        run_command.append(f'--icon={win_icon}')
    else:
        raise NotImplementedError("Platform is not supported for creating a MAP Client application.")

    run_command.append(os.pathsep.join([f'--add-binary={rcc_exe}', os.path.join(*pyside_resource_tool_dir, '')]))
    run_command.append(os.pathsep.join([f'--add-binary={uic_exe}', os.path.join(*pyside_resource_tool_dir, '')]))

    externally_specified_internal_workflows_zip = os.environ.get('INTERNAL_WORKFLOWS_ZIP', '<not-a-file>')
    if os.path.isfile(externally_specified_internal_workflows_zip):
        internal_workflows_zip = externally_specified_internal_workflows_zip
    else:
        internal_workflows_zip = os.path.abspath(os.path.join('..', '..', 'src', 'internal_workflows.zip'))

    if os.path.isfile(internal_workflows_zip):
        data = os.pathsep.join([internal_workflows_zip, '.'])
        run_command.append(f'--add-data={data}')

    plugin_paths_file = os.path.join(os.getcwd(), 'mapclientplugins_paths.json')
    site_packages_dir = site.getsitepackages()[0]

    if os.path.isfile(plugin_paths_file):
        with open(plugin_paths_file) as fh:
            content = json.load(fh)

        for plugin_path, mode in content.items():
            run_command.append(f'--paths={plugin_path}')
            if mode == 'requirements_file':
                _create_plugin_ns_pth_file(plugin_path, site_packages_dir)
                _create_egg_info_directory(plugin_path)

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
