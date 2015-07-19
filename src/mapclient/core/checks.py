'''
Created on Jun 26, 2015

@author: hsorby
'''
import subprocess
from mapclient.settings.definitions import GIT_EXE, VIRTUAL_ENV_PATH, \
    PYSIDE_UIC_EXE, PYSIDE_RCC_EXE
import os.path
from mapclient.core.utils import which

class ApplicationChecks(object):
    '''
    classdocs
    '''


    def __init__(self, options):
        '''
        Constructor
        '''
        self._options = options
        self._report = 'Failure: This test failed'

    def doCheck(self):
        return False

    def report(self):
        return self._report


class WizardToolChecks(ApplicationChecks):

    title = 'Wizard Tool'

    def doCheck(self):
        uic_result = False
        rcc_result = False
        self._report = ''  # {0}\n'.format(self.title)
        try:
            pyside_uic = self._options[PYSIDE_UIC_EXE]
            p = subprocess.Popen([pyside_uic, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = p.communicate()
            return_code = p.returncode
            if return_code == 0:
                uic_result = True
                self._report += "'{0}' successfully ran.".format(pyside_uic)
            else:
                self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(pyside_uic, return_code)
        except Exception as e:
            self._report += "'{0}' did not execute successfully, caused exception:\n{1}".format(pyside_uic, e)
        try:
            pyside_rcc = self._options[PYSIDE_RCC_EXE]
            p = subprocess.Popen([pyside_rcc, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = p.communicate()
            return_code = p.returncode
            # pyside-rcc returns 1 for all program executions that don't actual compile resources.
            if return_code == 1 and 'Resource Compiler for Qt version' in stderr.decode('utf-8'):
                rcc_result = True
                self._report += "'{0}' successfully ran.".format(pyside_rcc)
            else:
                self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(pyside_rcc, return_code)
        except Exception as e:
            self._report += "'{0}' did not execute successfully, caused exception:\n{1}".format(pyside_rcc, e)

        return uic_result and rcc_result


class VirtualEnvChecks(ApplicationChecks):

    title = 'Virtual Environment'

    def _testPipExe(self, venv_path):
        pip_exe = which(os.path.join(venv_path, 'bin', 'pip'))
        return pip_exe is not None

    def doCheck(self):
        venv_path = self._options[VIRTUAL_ENV_PATH]
        result = False
        if ' ' in venv_path or not venv_path:
            self._report = "'{0}' is not a valid virtual environment path.".format(venv_path)
        elif not self._testPipExe(venv_path):
            self._report = "'{0}' is not a valid pip executable.".format(os.path.join(venv_path, 'bin', 'pip'))
        else:
            result = True
            self._report = "'{0}' is a valid virtual environment.".format(venv_path)

        return result


class VCSChecks(ApplicationChecks):

    title = 'Version Control'

    def doCheck(self):
        result = False
        self._report = ''
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

        return result

def runChecks(options):
    checks_wizard = WizardToolChecks(options)
    if not checks_wizard.doCheck():
        return False

    checks_venv = VirtualEnvChecks(options)
    if not checks_venv.doCheck():
        return False

    checks_vcs = VCSChecks(options)
    if not checks_vcs.doCheck():
        return False

    return True


