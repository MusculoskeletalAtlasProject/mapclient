"""
Created on Jun 26, 2015

@author: hsorby
"""
import logging
import subprocess
import os.path
import platform

from PySide2 import QtCore

from mapclient.settings.definitions import GIT_EXE, \
    PYSIDE_RCC_EXE, PYSIDE_UIC_EXE, USE_EXTERNAL_GIT, INTERNAL_EXE, \
    USE_EXTERNAL_RCC, USE_EXTERNAL_UIC
from mapclient.core.utils import which, qt_tool_wrapper


logger = logging.getLogger(__name__)


class ApplicationChecks(object):

    def __init__(self, options):
        self._options = options
        self._report = 'Failure: This test failed'

    def doCheck(self):
        return False

    def report(self):
        return self._report


class WizardToolChecks(ApplicationChecks):

    title = 'Wizard Tool'

    def _check_rcc(self):
        if self._options[USE_EXTERNAL_RCC]:
            return_code, msg = qt_tool_wrapper(self._options[PYSIDE_RCC_EXE], ['-version'], True)
        else:
            return_code, msg = qt_tool_wrapper("rcc", ['-version'])

        return return_code == 0, msg

    def _check_uic(self):
        if self._options[USE_EXTERNAL_UIC]:
            return_code, msg = qt_tool_wrapper(self._options[PYSIDE_UIC_EXE], ['-version'], True)
        else:
            return_code, msg = qt_tool_wrapper("uic", ['-version'])

        return return_code == 0, msg

    def doCheck(self):
        self._report = ''  # {0}\n'.format(self.title)
        rcc_result, msg= self._check_rcc()
        if rcc_result:
            self._report += "Resource compiler successfully ran."
        else:
            self._report += "Resource compiler reported error: {0}".format(msg)
        uic_result, msg = self._check_uic()
        if uic_result:
            self._report += "User interface compiler successfully ran."
        else:
            self._report += "User interface compiler reported error: {0}".format(msg)

        return rcc_result and uic_result


class VCSChecks(ApplicationChecks):

    title = 'Version Control'

    def doCheck(self):
        result = False
        self._report = ''

        if self._options[USE_EXTERNAL_GIT]:
            try:
                vcs_tool = self._options[GIT_EXE]
                p = subprocess.Popen([vcs_tool, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = p.communicate()
                return_code = p.returncode
                if return_code == 0 and 'git version' in stdout.decode('utf-8'):
                    result = True
                    self._report += "'{0}' successfully ran.".format(vcs_tool)
                else:
                    self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(vcs_tool, return_code)
            except Exception as e:
                self._report += "'{0}' did not execute successfully, caused exception:\n{1}".format(vcs_tool, e)
        else:
            try:
                import dulwich
                ver = dulwich.__version__
                self._report += "Internal Git version '{0}.{1}.{2}' successfully ran.".format(ver[0], ver[1], ver[2])
                result = True
            except ImportError:
                self._report += "Internal Git did not execute successfully."

        return result


def runChecks(options):
    check_status = True
    checks_wizard = WizardToolChecks(options)
    if not checks_wizard.doCheck():
        check_status = False

    checks_vcs = VCSChecks(options)
    if not checks_vcs.doCheck():
        check_status = False

    return check_status


def getPipExecutable(venv_path):
    python_version = platform.python_version_tuple()
    if os.name == 'nt':
        int_directory = 'Scripts'
    else:
        int_directory = 'bin'
    pip_exe = which(os.path.join(venv_path, int_directory, 'pip' + python_version[0] + '.' + python_version[1]))
    return pip_exe


def getActivateScript(venv_path):
    if os.name == 'nt':
        int_directory = 'Scripts'
        suffix = '.bat'
    else:
        int_directory = 'bin'
        suffix = ''
    activate_script = which(os.path.join(venv_path, int_directory, 'activate' + suffix))
    return activate_script
