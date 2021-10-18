import sys
import json
import requests

from urllib.parse import parse_qs, quote_plus
      
from tools.pmr.jsonclient.credential import OAuthCredential

_PROTOCOL = 'application/vnd.physiome.pmr2.json.0'
_UA = 'pmr.jsonclient.Client/0.2'

_DEFAULT_SCOPE = '{0}/scope/collection,{0}/scope/search,{0}/scope/workspace_full'

def std_headers():
    h = {'Accept': _PROTOCOL,
         'Content-Type': _PROTOCOL,
         'User-Agent': _UA}
    return h


class Client(object):

    _site = None
    _auth = None
    
    lasturl = None
    consumer = None
    token = None
    request_token = None
    dashboard = None

    def __init__(self, website_address, consumer_keys, user_keys):
        self._site = 'http://' + website_address
        self._credential = OAuthCredential(consumer_keys, user_keys)
        self._scope = _DEFAULT_SCOPE.format(self._site)
        self.mismatched_content = None
        
    def hasAccess(self):
        return self._credential.hasAccess()
    
    def clearAccess(self):
        self._credential.clearAccess()
    
    def access(self):
        return self._credential.access()
    
    def search(self, text):
        """ This is a Plone style search so wildcards are necessary.
        """
        url = '%s/search' % self._site
        headers = std_headers()
        if self.hasAccess():
            headers.update(self._credential.getAuthorization('POST', url))
            
        data = {'SearchableText': text, 'portal_type': 'Workspace'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        return response.json()
    
    def addWorkspace(self, title=None, description=None):
        url = '%s/workspace/+/addWorkspace' % self._site
        if not self.hasAccess():
            return ''
        
        headers = std_headers()
        headers.update(self._credential.getAuthorization('POST', url))
        data = {}
        data['actions'] = {'add': '1'}
        data['fields'] = {'storage': 'git', 'description': description, 'title': title}
        response = requests.post(url, headers=headers, data=json.dumps(data), allow_redirects=False)
        
        return response.headers['Location']
    
    def requestTemporaryCredential(self):
        url = '%s/%s?scope=%s' % (self._site, OAuthCredential._REQUEST_TOKEN, quote_plus(self._scope))
        
        headers = self._credential.getAuthorization('GET', url, callback='oob')
        response = requests.get(url, headers=headers)
        response_dict = parse_qs(response.text)
        key = response_dict.get('oauth_token', ['']).pop()
        secret = response_dict.get('oauth_token_secret', ['']).pop()
        self._credential.setAccess(key, secret)
        
        return key
    
    def setPermanentCredential(self, verifier):
        # Assume self.key is a request token key.
        url = '%s/%s' % (self._site, OAuthCredential._GET_ACCESS_TOKEN)

        headers = self._credential.getAuthorization('GET', url, verifier=verifier)
        response = requests.get(url, headers=headers)
        response_dict = parse_qs(response.text)
        key = response_dict.get('oauth_token', ['']).pop()
        secret = response_dict.get('oauth_token_secret', ['']).pop()
        self._credential.setAccess(key, secret)
        
    def authorizationUrl(self, key):
        return '%s/%s?oauth_token=%s' % (self._site, OAuthCredential._AUTHORIZE_TOKEN, key)
    
    def setSite(self, site):
        self._site = site
        self.updateDashboard()

    def setCredential(self, credential, update=False):
        # XXX figure out some way to do the update smartly, such as test
        # whether the credentials are ready to be used.
        self._credential = credential
        self._credential.setPMR2Client(self)
        if update:
            self.updateDashboard()

    def updateDashboard(self):
        url = '%s/pmr2-dashboard' % self._site
        headers = std_headers()
        result = requests.get(url, headers=headers)
        self.dashboard = result.json()

    def getDashboard(self):
        if self.dashboard is None:
            self.updateDashboard()
        return self.dashboard

    def getDashboardMethod(self, name):
        action = self.dashboard[name]
        # Can't have unicode.
        url = str(action['target'])
        response = self.getResponse(url)
        # Uhh this will have a reference to this object, maybe track
        # that somehow?
        return Method(self, self.lasturl, response)


class Method(object):

    def __init__(self, context, url, obj):
        self.context = context
        self._obj = obj
        self.url = url

    def raw(self):
        return self._obj

    def fields(self):
        if isinstance(self._obj, dict):
            return self._obj.get('fields', {})
        return {}

    def actions(self):
        if isinstance(self._obj, dict):
            return self._obj.get('actions', {})
        return {}

    def errors(self):
        fields = self.fields()
        errors = []
        for name, field in fields.items():
            error = field.get('error', '')
            if error:
                errors.append((name, error))
        return errors

    def post(self, action, fields):
        data = {}
        data['actions'] = {action: '1'}
        data['fields'] = fields
        result = self.context.getResponse(self.url, data)
        self.__init__(self.context, self.context.lasturl, result)
        return result
