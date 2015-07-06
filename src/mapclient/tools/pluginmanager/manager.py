'''
Created on May 19, 2015

@author: hsorby
'''
import os, sys
import logging
import subprocess

from mapclient.core.utils import which
from mapclient.settings.definitions import VIRTUAL_ENV_PATH, \
    VIRTUAL_ENV_SETUP_ATTEMPTED

logger = logging.getLogger(__name__)

def getVirtualEnvCandidates():
    """Return a list of strings which contains possible names
    of the virtualenv program for this environment.
    """
    if sys.version_info < (3, 0):
        virtualenv_candidates = ['virtualenv', 'virtualenv2']
    else:
        virtualenv_candidates = ['virtualenv', 'virtualenv3']

    return virtualenv_candidates


class PluginManager(object):
    '''
    Plugin Manager class
    '''


    def __init__(self, options):
        '''
        Constructor
        '''
        self._virtualenv_dir = options[VIRTUAL_ENV_PATH]
        self._setup_attempted = options[VIRTUAL_ENV_SETUP_ATTEMPTED]

    def setupFailed(self):
        """
        Check whether the setup of the virtual environment failed.
        The first time the application is started it will attempt to create
        a virtual environment for the MAP Client plugins, if this fails then
        this method will return True.  If no virtual environment setup has
        been attempted then this method will return False.
        """
        return self._setup_attempted

    def exists(self):
        return os.path.exists(os.path.join(self._virtualenv_dir, 'bin'))

    def list(self):
        pip_exe = which(os.path.join(self._virtualenv_dir, 'bin', 'pip'))

        install_list = subprocess.check_output([pip_exe, 'list'])
        install_list = install_list.decode('utf-8')

        return install_list

    def setup(self):
        for candidate in getVirtualEnvCandidates():
            try:
                p = subprocess.Popen([candidate, '--clear', '--system-site-packages', self._virtualenv_dir],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()

                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.error(stderr)
            except SyntaxError:
                pass

    def addSitePackages(self):
        '''
        Append the site-packages directory of the virtual
        environment to the system path
        '''
        site_packages_path = None
        for root, _, _ in os.walk(self._virtualenv_dir , topdown=False):
            if root.endswith('site-packages'):
                site_packages_path = root
                break

        if site_packages_path:
            sys.path.append(site_packages_path)
        else:
            logger.warning('Site packages directory not added to sys.path.')

    def _loadWorkflowPlugins(self, wf_location):
        wf = _getWorkflowConfiguration(wf_location)

        return PluginDatabase.load(wf)

    def checkPlugins(self, wf_location):
        required_plugins = self._loadWorkflowPlugins(wf_location)
        missing_plugins = self._plugin_database.checkForMissingPlugins(required_plugins)
        return missing_plugins

    def checkDependencies(self, wf_location):
        required_plugins = self._loadWorkflowPlugins(wf_location)
        virtenv_dir = getVirtEnvDirectory()
        vem = PluginManager(virtenv_dir)
        missing_dependencies = {}
        if vem.exists():
            missing_dependencies = self._plugin_database.checkForMissingDependencies(required_plugins, vem.list())
        return missing_dependencies


