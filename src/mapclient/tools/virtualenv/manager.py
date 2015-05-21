'''
Created on May 19, 2015

@author: hsorby
'''
import os, sys
import logging
import subprocess

from mapclient.core.utils import which

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


class VirtualEnvManager(object):
    '''
    VirtualEnv Manager class
    '''


    def __init__(self, virtualenv_dir):
        '''
        Constructor
        '''
        self._virtualenv_dir = virtualenv_dir
        
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

        sys.path.append(site_packages_path)

