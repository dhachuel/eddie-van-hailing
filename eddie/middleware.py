from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import falcon

global EXEMPT_ROUTES, EXEMPT_METHODS
EXEMPT_ROUTES = [
    'quote',
    'trip',
    'rider'
]
EXEMPT_METHODS = [

]


class AuthMiddleware(object):
    """

    """

    def process_request(self, req, resp):
        token = req.get_header('Authorization')

        for exempt_path in EXEMPT_ROUTES:
            if exempt_path in req.path:
                return

        for exempt_method in EXEMPT_METHODS:
            if req.method == exempt_method:
                return

        if token is None or not self._token_is_valid():
            raise falcon.HTTPUnauthorized(description='Auth token required')

    def _token_is_valid(self):
        return(True) # You should do this better