import sys

from oauthlib.oauth1 import Client


def safe_unicode(s):
    # workaround for unicode requirements
    if sys.version < '3':
        if s:
            import codecs
            return codecs.unicode_escape_decode(s)[0]

    return s


class Credential(object):
    """
    Credential to access a site.  Ideally this should all integrate
    somehow with urllib2.
    """

    pmr2_client = None

    def getAuthorization(self, request):
        """
        Subclass will implement the method to return the authorization
        header.
        """

        raise NotImplementedError()

    def apply(self, request):
        auth = self.getAuthorization(request)
        if auth:
            request.add_header('Authorization', auth)

    def setPMR2Client(self, pmr2_client):
        self.pmr2_client = pmr2_client

    def hasAccess(self):
        return False


class BasicCredential(Credential):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getAuthorization(self, request):
        return 'Basic ' + ('%s:%s' %
            (self.username, self.password)).encode('base64').strip()

    def hasAccess(self):
        return not (self.username is None or self.password is None)


class OAuthCredential(Credential):

    _REQUEST_TOKEN = 'OAuthRequestToken'
    _AUTHORIZE_TOKEN = 'OAuthAuthorizeToken'
    _GET_ACCESS_TOKEN = 'OAuthGetAccessToken'

    def __init__(self, consumer_keys, user_keys):
        """
        The OAuth credential provider for PMR2 JSON Client.

        oauth_client
            The client key/secret pair.
        oauth_access
            The access key/secret pair.
        """

        self.consumer_key, self.consumer_secret = consumer_keys
        # The reason why these are just simply called key/secret is due
        # to how they are reused for both temporary and access tokens.
        self.clearAccess()
        self.key, self.secret = user_keys

    def setAccess(self, key, secret):
        self.key, self.secret = key, secret
        
    def hasAccess(self):
        return not (self.key is None or self.secret is None)

    def clearAccess(self):
        self.key, self.secret = None, None

    def access(self):
        return (self.key, self.secret)
    
    def getAuthorization(self, method, url, callback=None, verifier=None):
        client = Client(
            safe_unicode(self.consumer_key),
            safe_unicode(self.consumer_secret),
            safe_unicode(self.key),
            safe_unicode(self.secret),
            callback_uri=safe_unicode(callback),
            verifier=safe_unicode(verifier),
        )
        safe_method = safe_unicode(method)
        safe_url = safe_unicode(url)
        # data is omitted because no www-form-encoded data
        _, header, _ = client.sign(safe_url, safe_method)
        return header

