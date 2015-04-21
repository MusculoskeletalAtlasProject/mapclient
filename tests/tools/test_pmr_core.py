from unittest import TestCase

from mapclient.tools.pmr.core import TokenHelper


class DummySession(object):

    def __init__(self, targets):
        self.targets = targets

    def fetch_request_token(self, target):
        self.targets.append(target)
        return {
            'oauth_token': 'dummy_request',
            'oauth_token_secret': 'dummy_secret',
        }

    def fetch_access_token(self, target):
        self.targets.append(target)
        return {
            'oauth_token': 'dummy_access',
            'oauth_token_secret': 'dummy_access_secret',
        }


class DummySessionFactory(object):

    def __call__(self, *a, **kw):
        self.args = (a, kw)
        self.targets = []
        return DummySession(self.targets)


class TokenHelperTestCase(TestCase):

    def setUp(self):
        self.helper = TokenHelper('client_key', 'client_secret')
        self.dsf = DummySessionFactory()
        self.helper.oauth_session_cls = self.dsf

    def test_get_temporary_credentials(self):
        result = self.helper.get_temporary_credentials()
        self.assertEqual(self.dsf.args, ((), {
            'callback_uri': 'oob',
            'client_key': 'client_key',
            'client_secret': 'client_secret'
        }))

        self.assertEqual(result, ('dummy_request', 'dummy_secret'))
        self.assertTrue(self.dsf.targets[0].startswith(
            'https://models.physiomeproject.org/OAuthRequestToken?scope='
        ))

    def test_get_authorize_url(self):
        # need temporary creds first.
        self.assertRaises(ValueError, self.helper.get_authorize_url)

        self.helper.get_temporary_credentials()
        result = self.helper.get_authorize_url()
        self.assertEqual(result,
            'https://models.physiomeproject.org/'
                'OAuthAuthorizeToken?oauth_token=dummy_request')

    def test_get_token_credentials(self):
        self.helper.request_token = 'test_request'
        self.helper.request_secret = 'test_secret'
        self.assertRaises(ValueError, self.helper.get_token_credentials)

        self.helper.set_verifier('test_verifier')
        result = self.helper.get_token_credentials()
        self.assertEqual(self.dsf.args, ((), {
            'client_key': 'client_key',
            'client_secret': 'client_secret',
            'resource_owner_key': 'test_request',
            'resource_owner_secret': 'test_secret',
            'verifier': 'test_verifier',
        }))

        self.assertEqual(result, {
            'oauth_token': 'dummy_access',
            'oauth_token_secret': 'dummy_access_secret',
        })
        self.assertEqual(self.dsf.targets[0],
            'https://models.physiomeproject.org/OAuthGetAccessToken')
