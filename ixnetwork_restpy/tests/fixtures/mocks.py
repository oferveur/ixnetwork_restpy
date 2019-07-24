"""Mocks all request/responses needed for unit tests
"""

class Mocks(object):
    PLATFORMS =  {
        'windows': 'SelfHost',
        'linux': 'Jetty',
        'connection_manager': 'Microsoft-HTTPAPI/2.0'
    }
    _PLATFORM = 'windows'

    REQUEST_RESPONSE = {
        'api/v1/sessions': {
            'GET': {
                'data': [
                    {
                        'href': 'api/v1/sessions/1',
                        'id': '1',
                        'userId': 'admin',
                        'userName': 'admin',
                        'applicationType': 'ixnetwork',
                        'state': 'ACTIVE'
                    }
                ],
                'status_code': 200
            }
        },
        'api/v1/auth/session' : {
            'GET': {
                'data': {
                    'apiKey': '0000000000000000',
                    'trace': 'request_response',
                    'userName': 'admin'
                },
                'status_code': 200
            },
            'POST': {
                'data': None,
                'status_code': 200
            }
        },
        'api/v1/sessions/1/ixnetwork': {
            'GET': {
                'data': {
                    'href': 'api/v1/sessions/1/ixnetwork'
                },
                'status_code': 200
            }
        },
        'api/v1/sessions/1/ixnetwork/globals': {
            'GET': {
                'data': {
                    'href': 'api/v1/sessions/1/ixnetwork/globals',
                    'buildNumber': '9.00.0.1314'
                },
                'status_code': 200
            }
        }
    }

    @staticmethod
    def set_platform(platform = 'windows'):
        """
        Args:
            platform (windows | linux | connection_manager)
        """
        Mocks._PLATFORM = platform

    @staticmethod
    def mocked_request(**kwargs):
        class MockResponse:
            def __init__(self, response):
                self.json_data = response['data']
                self.status_code = response['status_code']
                self.headers = {
                    'server': Mocks.PLATFORMS[Mocks._PLATFORM]
                }
                if self.json_data is not None:
                    self.headers['Content-Type'] = 'application/json'

            def json(self):
                return self.json_data

        class MockResponseError:
            def __init__(self, url, exception):
                self.status_code = 404
                self.url = url
                self.reason = 'Not Found'
                self.text = str(exception)

        try:
            start = kwargs['url'].find('api/v1')
            method = kwargs['method']
            request = kwargs['url'][start:]
            request_response = Mocks.REQUEST_RESPONSE[request]
            return MockResponse(request_response[method])
        except Exception as e:
            return MockResponseError(request, e)

    def __init__(self):
        pass