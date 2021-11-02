import os
import platform
import PySide2 as RefMod
import PyInstaller.__main__

variant = '-mapping-tools'

here = os.path.dirname(__file__)

run_command = [
    '../../src/mapclient/application.py',
    '-n', f'MAP-Client{variant}',
    '--debug', 'noarchive',
    '--windowed',
    '--noconfirm',
    '--hidden-import', 'scipy',
    '--hidden-import', 'scipy.interpolate',
    '--hidden-import', 'numpy',
    '--hidden-import', 'mapclientplugins',
    '--hidden-import', 'opencmiss.utils',
    '--hidden-import', 'opencmiss.zincwidgets',
    '--additional-hooks-dir=hooks',
]


images_dir = os.path.join('..', '..', 'src', 'mapclient', 'tools', 'pluginwizard', 'qt', 'images')
names = os.listdir(images_dir)
for name in names:
    data = os.pathsep.join([os.path.join(os.path.abspath(images_dir), name), os.path.join('res', 'images')])
    run_command.append(f'--add-data={data}')

if platform.system() == 'Darwin':
    pyside_dir = os.path.dirname(RefMod.__file__)
    rcc_exe = os.path.join(pyside_dir, "rcc")
    uic_exe = os.path.join(pyside_dir, "uic")
    rel_rcc_exe = os.path.relpath(rcc_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))
    rel_uic_exe = os.path.relpath(uic_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))

    macos_icon = os.path.join('..', 'macos', 'MAP-Client.icns')
    run_command.append(f'--icon={macos_icon}')

    run_command.append(f'--add-binary={rel_rcc_exe}:PySide2/')
    run_command.append(f'--add-binary={rel_uic_exe}:PySide2/')
elif platform.system() == "Windows":
    win_icon = os.path.join('..', 'win', 'MAP-Client.ico')
    run_command.append(f'--icon={win_icon}')

internal_workflows_zip = os.path.abspath(os.path.join('..', '..', 'src', 'internal_workflows.zip'))
if os.path.isfile(internal_workflows_zip):
    data = os.pathsep.join([internal_workflows_zip, '.'])
    run_command.append(f'--add-data={data}')

print('Running command: ', run_command)
PyInstaller.__main__.run(run_command)
