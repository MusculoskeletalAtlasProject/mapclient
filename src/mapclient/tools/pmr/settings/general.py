"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""

from PySide2 import QtCore

# Credentials follows:
#
# Key    OP8AKmDIlH7OkHaPWNbnb-zf
# Secret    QQcKMnyCjjb7JNDHA-Lwdu7p
#
# The scope that should be used
#
# from urllib import quote_plus
# DEFAULT_SCOPE = quote_plus(
#     'http://localhost:8280/pmr/scope/collection,'
#     'http://localhost:8280/pmr/scope/search,'
#     'http://localhost:8280/pmr/scope/workspace_tempauth,'
#     'http://localhost:8280/pmr/scope/workspace_full'
# )


class PMR(object):

    DEFAULT_PMR_IPADDRESS = 'http://teaching.physiomeproject.org'
    DEFAULT_CONSUMER_PUBLIC_TOKEN = 'OP8AKmDIlH7OkHaPWNbnb-zf'
    DEFAULT_CONSUMER_SECRET_TOKEN = 'QQcKMnyCjjb7JNDHA-Lwdu7p'

    def __init__(self):
        self._instances = {}
        self.readSettings()

    def readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')
        # pmr_host?  this is a domain name...
        self._active_host = settings.value('active-pmr-website', self.DEFAULT_PMR_IPADDRESS)
        self._consumer_public_token = settings.value('consumer-public-token', self.DEFAULT_CONSUMER_PUBLIC_TOKEN)
        self._consumer_secret_token = settings.value('consumer-secret-token', self.DEFAULT_CONSUMER_SECRET_TOKEN)
        
        size = settings.beginReadArray('instances')
        for i in range(size):
            settings.setArrayIndex(i)
            host = settings.value('pmr-website')
            public_token = settings.value('user-public-token', None)
            secret_token = settings.value('user-secret-token', None)
            self._instances[host] = {'user-public-token': public_token, 'user-secret-token': secret_token}
        settings.endArray()
        
        settings.endGroup()
        self.addHost(self._active_host)

    def writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')
        
        settings.setValue('active-pmr-website', self._active_host)

        settings.beginWriteArray('instances')
        index = 0
        for key in self._instances:
            settings.setArrayIndex(index)
            settings.setValue('pmr-website', key)
            settings.setValue('user-public-token', self._instances[key]['user-public-token'] or '')
            settings.setValue('user-secret-token', self._instances[key]['user-secret-token'] or '')
            index += 1
        settings.endArray()

        settings.endGroup()
        
    def setActiveHost(self, uri):
        """
        if the uri argument is in the dict of instances it will
        set that host as the active host.  if the uri evaluates 
        to False the active host will be set to None.
        """
        status = False
        if uri in self._instances:
            self._active_host = uri
            status = True
        elif not uri:
            self._active_host = None
            status = True
            
        if status:
            self.writeSettings()
        
        return status
    
    def activeHost(self):
        return self._active_host
            
    def addHost(self, host):
        status = False
        if host not in self._instances and host:
            self._instances[host] = {'user-public-token': None, 'user-secret-token': None}
            self.writeSettings()
            status = True
            
        return status
    
    def count(self):
        return len(self._instances)
    
    def hosts(self):
        return iter(self._instances)
    
    def removeHost(self, host):
        status = False
        if host in self._instances:
            del self._instances[host]
            if self._active_host == host:
                self._active_host = None
                
            self.writeSettings()
            status = True
            
        return status
    
    def host(self):
        return self._active_host

    def update_token(self, oauth_token, oauth_token_secret):
        """
        update the oauth tokens for the currently active PMR target
        """
        if self._active_host is not None:
            self._instances[self._active_host]['user-public-token'] = oauth_token
            self._instances[self._active_host]['user-secret-token'] = oauth_token_secret
            self.writeSettings()

    def has_access(self):
        """
        return true if both the user tokens are something for the currently active 
        PMR target, false otherwise
        """
        if self._active_host is None:
            return False
        
        return bool(self._instances[self._active_host]['user-public-token'] and self._instances[self._active_host]['user-secret-token'])

    def get_session_kwargs(self):
        return {
            'client_key': self._consumer_public_token,
            'client_secret': self._consumer_secret_token,
            'resource_owner_key': self._instances[self._active_host]['user-public-token'],
            'resource_owner_secret': self._instances[self._active_host]['user-secret-token'],
        }
        
    def get_client_token_kwargs(self):
        return {
            'client_key': self._consumer_public_token,
            'client_secret': self._consumer_secret_token,
        }


