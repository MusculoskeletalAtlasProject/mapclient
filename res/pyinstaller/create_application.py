import os
import platform
import PySide2 as RefMod
import PyInstaller.__main__
from PyInstaller.utils.hooks import collect_data_files


here = os.path.dirname(__file__)
hooks_dir = os.path.join('..', 'res', 'pyinstaller', 'hooks')

run_command = [
    '../../src/mapclient/application.py',
    '-n', 'MAPClient',
    '--windowed',
    '--noconfirm',
    '--hidden-import', 'mapclientplugins',
    '--hidden-import', 'opencmiss.utils',
    '--hidden-import', 'opencmiss.zincwidgets',
    f'--additional-hooks-dir=hooks',
]


print('[[[[[[[[[[[[[[[[')
print(collect_data_files('mapclient', includes=['*.png']))
images_dir = os.path.join('..', '..', 'src', 'mapclient', 'tools', 'pluginwizard', 'qt', 'images')
names = os.listdir(images_dir)
for name in names:
    data = os.pathsep.join([os.path.join(os.path.abspath(images_dir), name), os.path.join('res', 'images')])
    run_command.append(f'--add-data={data}')
print(names)
print(os.pathsep)
# for d in opencmiss.__path__:
#     run_command.append(f'--path={d}')
#
# for d in mapclientplugins.__path__:
#     run_command.append(f'--path={d}')

if platform.system() == 'Darwin':
    pyside_dir = os.path.dirname(RefMod.__file__)
    rcc_exe = os.path.join(pyside_dir, "rcc")
    uic_exe = os.path.join(pyside_dir, "uic")
    rel_rcc_exe = os.path.relpath(rcc_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))
    rel_uic_exe = os.path.relpath(uic_exe, here)  # os.path.join(here, 'dist', 'MAPClient'))

    run_command.append(f'--add-binary={rel_rcc_exe}:PySide2/')
    run_command.append(f'--add-binary={rel_uic_exe}:PySide2/')

print('Running command: ', run_command)
PyInstaller.__main__.run(run_command)
# mapclient/application.py -n MAPClient --hidden-import opencmiss.zinc --windowed -i ../res/win/MAP-Client.ico --hidden-import opencmiss