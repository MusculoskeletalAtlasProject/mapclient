#-----------------------------------------------------------------------------
# Copyright (c) 2013-2017, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
# If numpy is built with MKL support it depends on a set of libraries loaded
# at runtime. Since PyInstaller's static analysis can't find them they must be
# included manually.
#
# See
# https://github.com/pyinstaller/pyinstaller/issues/1881
# https://github.com/pyinstaller/pyinstaller/issues/1969
# for more information
import os
import os.path
import re
from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging 
from PyInstaller import compat
from setuputils import which
import opencmiss.iron

binaries = []

# print('========================IRON==========================')
binaries = []

iron_dlls = []
iron_dll = which('iron.dll')
iron_dlls += iron_dll
iron_c_dll = which('iron_c.dll')
iron_dlls += iron_c_dll

additional_dlls = []
msmpi_dll = which('msmpi.dll')
additional_dlls += msmpi_dll


binaries += [(dll, '') for dll in iron_dlls]
binaries += [(dll, '') for dll in additional_dlls]
