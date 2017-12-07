from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from eddie.db_client import *
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
        for exempt_path in EXEMPT_ROUTES:
            if exempt_path in req.path:
                return

        for exempt_method in EXEMPT_METHODS:
            if req.method == exempt_method:
                return

        if self._is_user_valid(req):
            raise falcon.HTTPUnauthorized(description='valid user required')

    def _is_user_valid(self, req):
        """
        Checks if the given request is from a valid user, i.e the user's id is in the rider or driver database
        :param req: The given request object
        :return: True iff the given request is from a valid user
        """
        # Check if rider
        user_id = req.get_header('id')
        rdb_response = rdb.db('eddie').table('riders').get(user_id).run(rdb_conn)
        if len(rdb_response) > 0:
            return True # Rider found, reroute to rider endpoints

        # Check if driver
        rdb_response = rdb.db('eddie').table('drivers').get(user_id).run(rdb_conn)
        if len(rdb_response) > 0:
            return True # Driver found, reroute to rider endpoints

        return False