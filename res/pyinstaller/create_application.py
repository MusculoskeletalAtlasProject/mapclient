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

pyside_dir = os.path.dirname(RefMod.__file__)

if platform.system() == 'Darwin':
    rcc_exe = os.path.join(pyside_dir, "rcc")
    uic_exe = os.path.join(pyside_dir, "uic")

    macos_icon = os.path.join('..', 'macos', 'MAP-Client.icns')
    run_command.append(f'--icon={macos_icon}')

elif platform.system() == "Windows":
    rcc_exe = os.path.join(pyside_dir, "rcc.exe")
    uic_exe = os.path.join(pyside_dir, "uic.exe")

    win_icon = os.path.join('..', 'win', 'MAP-Client.ico')
    run_command.append(f'--icon={win_icon}')
else:
    raise NotImplementedError("Platform is not supported for creating a MAP Client application.")

rel_rcc_exe = os.path.relpath(rcc_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))
rel_uic_exe = os.path.relpath(uic_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))

run_command.append(os.pathsep.join([f'--add-binary={rel_rcc_exe}', 'PySide2/']))
run_command.append(os.pathsep.join([f'--add-binary={rel_uic_exe}', 'PySide2/']))

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
