"""
This is a setup.py script for creating a windows application using py2exe.
It is only suitable for using with version 3 of Python.

I had to fix a bug in the deprecated 'imp' module.  In the load_package function
the path gets appended to instead of starting from the original path.  Code added was

        orig_path = path[:]
        for extension in extensions:
            path = os.path.join(orig_path, '__init__'+extension)

in imp.py line 205.

This script also creates an installable executable using NSIS.  If NSIS is available (default location is
c:\\Program Files (x86)\\NSIS\\makensis.exe) then the output will be created in a directory 'package'.  The
nsis build can only be built after the py2exe build has successfully run.

Usage:
    python setup.py2exe.py py2exe
    python setup.py2exe.py nsis
"""
import os
import sys
from setuptools import setup, find_packages
from setuputils import which
from py2exe.distutils_buildexe import py2exe as build_py2exe
import pkgutil
from importlib.machinery import OPTIMIZED_BYTECODE_SUFFIXES
import py_compile
import glob
import virtualenv_support
import subprocess
import tempfile
import py2exe
import matplotlib

# Py2exe needs some help when importing packages from namespace packages
# by pre-importing them.
import opencmiss
import pmr2
import pmr2.wfctrl

from PySide import QtCore

from mapclient.settings import version as app_version

python_dir = os.path.dirname(sys.executable)

inbuilt_modules = os.listdir(os.path.join(python_dir, 'Lib'))
if 'site-packages' in inbuilt_modules:
    inbuilt_modules.remove('site-packages')
if 'test' in inbuilt_modules:
    inbuilt_modules.remove('test')

inbuilt_modules.append('virtualenv')
inbuilt_modules = [os.path.splitext(mod)[0] if mod.endswith('.py') else mod for mod in inbuilt_modules]

inbuilt_dlls = os.listdir(os.path.join(python_dir, 'DLLs'))
inbuilt_dlls = [os.path.join(python_dir, 'DLLs', dll) for dll in inbuilt_dlls if dll.endswith('.pyd')]

required_builtin_dlls = ['_ctypes.pyd', '_socket.pyd', '_ssl.pyd', 'pyexpat.pyd', 'select.pyd', 'unicodedata.pyd']
required_builtin_dlls = [os.path.join(python_dir, 'DLLs', dll) for dll in required_builtin_dlls]

support_files_virtualenv = [fn for fn in glob.glob(os.path.join(os.path.dirname(virtualenv_support.__file__), '*'))
                            if not os.path.basename(fn).startswith('__pycache__')]

support_files_lib2to3 = ['Grammar.txt', 'Grammar3.5.1.final.0.pickle', 'PatternGrammar.txt', 'PatternGrammar3.5.1.final.0.pickle']
support_files_lib2to3 = [os.path.join(python_dir, 'Lib', 'lib2to3', f) for f in support_files_lib2to3]

# Version, this should match the value in mapclient.settings.version
version = app_version.__version__

# Define the list of requirments
install_requires = ['rdflib',
                    'virtualenv',
                    'python-dateutil',
                    'pmr2.client',
                    ]

additional_dlls = []
# Assuming that we are using the mkl libraries from intel
mkl_core = which('mkl_core.dll')
mkl_def = which('mkl_def.dll')
mkl_intel_thread = which('mkl_intel_thread.dll')
libiomp5md = which('libiomp5md.dll')
additional_dlls.extend([mkl_core, mkl_def, mkl_intel_thread, libiomp5md])

# Assuming that we are using mpich2, what test can we perform to confirm this?
fmpich2 = which('fmpich2.dll')
# libiomp5md = which('libiomp5md.dll')
mpich2mpi = which('mpich2mpi.dll')
mpich2nemesis = which('mpich2nemesis.dll')
additional_dlls.extend([fmpich2, mpich2mpi, mpich2nemesis])
# If visual Studio 2015 need UCRTBASE.dll, but not for windows 10?
ucrtbase = which('ucrtbase.dll')
msvcp140 = which('msvcp140.dll')
concrt140 = which('concrt140.dll')
additional_dlls.extend([ucrtbase, msvcp140, concrt140])

# QtXml4 is required for resource compilers
qtxml4 = which('QtXml4.dll')
additional_dlls.extend([qtxml4])

additional_dlls = [dll[0] for dll in additional_dlls if dll]

pyside_compilers = []
pyside_uic = which('pyside-uic.exe')
pyside_uic_script = which('pyside-uic-script.py')
qtcore_file = QtCore.__file__
qt_dir = os.path.dirname(qtcore_file)
pyside_rcc = [qt_dir + '/pyside-rcc.exe']

pyside_compilers.extend(pyside_uic)
pyside_compilers.extend(pyside_uic_script)
pyside_compilers.extend(pyside_rcc)

APP = [
    {
        'script': 'mapclient/application.py',  # Main Python script.
        'icon_resources': [(0, '../res/win/MAP-Client.ico')],  # Icon to embed into the PE file.
        'dest_base' : 'MAP-Client',  # Name given to executable.
    },
]

wizard_image_files = glob.glob(os.path.join('mapclient', 'tools', 'pluginwizard', 'qt', 'images', '*.png'))

# site_packages_dir = site.getsitepackages()[1]
DATA_FILES = [('.', additional_dlls), ('.', pyside_compilers), ('.', [sys.executable]),
              ('Include', []), (os.path.join('Lib', 'site-packages', 'virtualenv_support'), support_files_virtualenv),
              (os.path.join('res', 'images'), wizard_image_files), (os.path.join('tcl', 'tcl8.6'), []),
              (os.path.join('tcl', 'tk8.6'), []), ('DLLs', inbuilt_dlls),
              (os.path.join('Lib', 'lib2to3'), support_files_lib2to3)]
DATA_FILES.extend(matplotlib.get_py2exe_datafiles())

# Need to import opencmiss before the py2exe attempts to load it, possibly because of it being a namespace package
PACKAGES = find_packages(exclude=['tests', 'tests.*', ])
PACKAGES.extend(['numpy', 'scipy', 'gias2', 'pkg_resources',
                 'opencmiss', 'opencmiss.zinc', 'opencmiss.iron', 'rdflib',
                 'pmr2', 'pmr2.wfctrl'])
EXCLUDES = ['numpy.distutils.tests',]
INCLUDES = ['virtualenv', 'matplotlib.backends.backend_qt4agg']
OPTIONS = {'py2exe': {
        'packages': PACKAGES,
        'excludes': EXCLUDES,
        'includes': INCLUDES,
        'skip_archive': True,
        'compressed': False,
    }
}


def get_target_module_path(base_dir, module_path):
    target_module_path = module_path.replace(python_dir + '\\', '')
    target_module_path = os.path.join(base_dir, target_module_path)
    return target_module_path


def compile_module(base_dir, module_path, module_name):
    source_file = os.path.join(module_path, module_name + '.py')
    target_module_path = get_target_module_path(base_dir, module_path)
    compiled_file = os.path.join(target_module_path, module_name + OPTIMIZED_BYTECODE_SUFFIXES[0])
    py_compile.compile(source_file, compiled_file)


def compile_package_file(base_dir, module_path):
    source_file = os.path.join(module_path, '__init__.py')
    target_module_path = get_target_module_path(base_dir, module_path)
    compiled_file = os.path.join(target_module_path, '__init__' + OPTIMIZED_BYTECODE_SUFFIXES[0])
    if os.path.isfile(source_file):
        py_compile.compile(source_file, compiled_file)
    else:
        print('Trying to compile non-existent file: {0}'.format(source_file))


def recurse_through_packages(base_dir, packages_list):
    for ff, name, package in packages_list:
        if not package:
            compile_module(base_dir, ff.path, name)
        else:
            take_copies_of = [(ff_next, name_next, package_next) for ff_next, name_next, package_next
                              in pkgutil.iter_modules([os.path.join(ff.path, name)])]
            recurse_through_packages(base_dir, take_copies_of)
            compile_package_file(base_dir, os.path.join(ff.path, name))


def code_and_store_builtins(base_dir):
    take_copies_of = [(ff, name, package) for ff, name, package in pkgutil.iter_modules() if name in inbuilt_modules]
    recurse_through_packages(base_dir, take_copies_of)


def adjust_virtualenv_exe(base_dir):
    # Need to check if I found virtual env that matches the current sys executable
    virtualenv = which('virtualenv.exe')[0]
    with open(virtualenv, 'rb') as fr:
        contents = fr.read()
        contents = contents.replace(sys.executable.lower().encode('ascii'), b"python.exe")
        with open(os.path.join(base_dir, 'virtualenv.exe'), 'wb') as f:
            f.write(contents)


class py2exe(build_py2exe):

    def run(self):
        build_py2exe.run(self)

        # Change location of Python executable in virtualenv script.
        adjust_virtualenv_exe(self.dist_dir)

        # Get built-ins compiled for virtualenv.
        code_and_store_builtins(self.dist_dir)

        # # Create orig prefix file
        # with open(os.path.join(self.dist_dir, 'Lib', 'orig-prefix.txt'), 'w') as f:
        #     pass


class ReplaceOnlyDict(dict):

    def __missing__(self, key):
        return '{' + key + '}'


class nsis(build_py2exe):

    def run(self):
        # Try to find makensis or use default location if not on the path.
        nsis_default_location = "c:\\Program Files (x86)\\NSIS\\makensis.exe"
        makensis = which("makensis.exe")
        if not makensis:
            makensis = nsis_default_location

        # Create package directory for output
        if not os.path.exists('package'):
            os.mkdir('package')

        # Create NSIS script from template
        with tempfile.NamedTemporaryFile(delete=False) as outputfile:
            with open('../res/win/nsis.nsi.template') as f:
                contents = f.read()

            match_keys = ReplaceOnlyDict(map_client_version=version,
                                         dist_dir=os.path.abspath(self.dist_dir),
                                         win_res_dir=os.path.abspath('../res/win/'),
                                         package_dir=os.path.abspath('package'))
            formatted_contents = contents.format_map(match_keys)
            outputfile.write(formatted_contents.encode())
            outputfile.flush()
            subprocess.call([makensis, outputfile.name])

        if os.path.isfile(outputfile.name):
            os.remove(outputfile.name)


setup(
    console=APP,
    options=OPTIONS,
    data_files=DATA_FILES,
    install_requires=install_requires,
    cmdclass={'py2exe': py2exe, 'nsis': nsis}
    # zipfile=None,
)

