import requests
import json
from django.test import TestCase, Client
from simpleauth.settings import get_env_variable


def get_access_token():
    """
    return: a dict in the form {'access_token': string, 'expires_in': int, 'token_type': string, 'scope': 'string, 'refresh_token': string}
    """
    response = requests.post(
        auth=requests.auth.HTTPBasicAuth(get_env_variable('ONA_CLIENT_ID'), get_env_variable('ONA_CLIENT_SECRET')),
        url="https://api.ona.io/o/token/",
        data={
            'grant_type': 'authorization_code',
            'code': get_env_variable('ONA_CLIENT_CODE'),
            'client_id': get_env_variable('ONA_CLIENT_ID'),
            'redirect_uri': 'https://2d50ff7a5358.ngrok.io/users/access-token-callback/'
        },
    )
    return json.loads(response.text)


class AuthTestCase(TestCase):
    access_token = None

    def setUp(self) -> None:
        self.client = Client()

    def test_basic_auth(self):
        """
        Test authentication using onadata username and onadata password
        """
        response = requests.get(
            url="https://api.ona.io/api/v1/",
            auth=requests.auth.HTTPBasicAuth(get_env_variable('ONA_USERNAME'), get_env_variable('ONA_PASSWORD'))
        )
        self.assertEqual(response.status_code, 200)

    def test_token_auth(self):
        """
        test authentication using a token given by onadata
        """
        token_data = get_access_token()
        response = requests.get(
            url="https://api.ona.io/api/v1/",
            headers={
                'Authorization': 'TempToken: {}'.format(token_data['access_token'])
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_access_ona_api_using_access_token(self):
        """
        Test accessing onadata using a token authorized request
        """
        token_data = get_access_token()
        response = requests.get(
            url="https://api.ona.io/api/v1/",
            headers={
                'Authorization': 'Bearer: {}'.format(token_data['access_token'])
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_cors_requests_to_ona_api(self):
        """
        Test access to cors protected resources using basic authenticated request
        """
        response = requests.get(
            url='https://api.ona.io/api/v1/user',
            auth=requests.auth.HTTPBasicAuth(get_env_variable('ONA_USERNAME'), get_env_variable('ONA_PASSWORD')),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)


