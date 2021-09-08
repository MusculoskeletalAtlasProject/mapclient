import logging

from urllib.parse import quote_plus

from requests_oauthlib.oauth1_session import OAuth1Session

logger = logging.getLogger(__name__)

DEFAULT_SITE_URL = 'https://models.physiomeproject.org'
TEACHING_SITE_URL = 'https://teaching.physiomeproject.org'

DEFAULT_SCOPE = (
    '{0}/pmr/scope/collection,'
    '{0}/pmr/scope/search,'
    '{0}/pmr/scope/workspace_tempauth,'
    '{0}/pmr/scope/workspace_full'
).format(DEFAULT_SITE_URL,)


class TokenHelper(object):

    request_token_endpoint = 'OAuthRequestToken'
    authorize_token_endpoint = 'OAuthAuthorizeToken'
    access_token_endpoint = 'OAuthGetAccessToken'

    oauth_session_cls = OAuth1Session

    def __init__(self, client_key, client_secret,
            request_token=None,
            request_secret=None,
            callback_url='oob',
            scope=DEFAULT_SCOPE,
            site_url=DEFAULT_SITE_URL,
            ):

        self.client_key = client_key
        self.client_secret = client_secret
        self.scope = scope
        self.site_url = site_url
        self.callback_url = callback_url
        self.request_token = request_token
        self.request_secret = request_secret
        self.verifier = None

    def get_temporary_credentials(self):
        target = '%(site_url)s/%(endpoint)s?scope=%(scope)s' % {
            'site_url': self.site_url,
            'endpoint': self.request_token_endpoint,
            'scope': quote_plus(self.scope),
        }

        oauth = self.oauth_session_cls(
            client_key=self.client_key,
            client_secret=self.client_secret,
            callback_uri=self.callback_url,
        )

        logger.debug('Requesting temporary credentials from %s', target)

        result = oauth.fetch_request_token(target)
        self.request_token = result.get('oauth_token')
        self.request_secret = result.get('oauth_token_secret')

        return self.request_token, self.request_secret

    def get_authorize_url(self):
        if not self.request_token:
            raise ValueError('no temporary credentials available')

        target = '%(site_url)s/%(endpoint)s?oauth_token=%(token)s' % {
            'site_url': self.site_url,
            'endpoint': self.authorize_token_endpoint,
            'token': self.request_token,
        }
        return target

    def set_verifier(self, verifier):
        self.verifier = verifier

    def get_token_credentials(self):
        if (not self.request_token or not self.request_secret or
                not self.verifier):
            raise ValueError('no temporary credentials available')

        target = '%(site_url)s/%(endpoint)s' % {
            'site_url': self.site_url,
            'endpoint': self.access_token_endpoint,
        }

        logger.debug('Requesting token credentials from %s', target)

        oauth = self.oauth_session_cls(
            client_key=self.client_key,
            client_secret=self.client_secret,
            resource_owner_key=self.request_token,
            resource_owner_secret=self.request_secret,
            verifier=self.verifier,
        )

        token = oauth.fetch_access_token(target)
        return token
