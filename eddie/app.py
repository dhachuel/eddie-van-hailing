##
## ENV SETUP
##
import falcon
import json
from jsonschema import validate, ValidationError
from eddie.db_client import *
from eddie.middleware import AuthMiddleware
from eddie.hooks import api_key, log_operation
from eddie.resources.quote import QuoteResource
from eddie.resources.trip import TripResource
from eddie.resources.rider import RiderResource
from eddie.resources.driver import DriverResource
from eddie.helpers import getReQLNow
import rethinkdb as rdb

##
## DECLARE API INSTANCE
##
api = falcon.API(
    middleware= AuthMiddleware()
)


##
## Session Resource
##
class SessionResource(object):

    @property
    def __post_request_schema(self):
        return (
            {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "user_type": {"type": "string", "value":["driver", "rider"]}
                }
            }
        )

    def on_post(self, req, resp):
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error',
                                   ex.message)

        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(
                falcon.HTTP_400,
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.'
            )

        # Validate request
        try:
            validate(result_json, self.__post_request_schema)
        except ValidationError as e:
            raise falcon.HTTPError(
                falcon.HTTP_400,
                'Request Format Error',
                e.message
            )

        # Look for active session
        check_if_email_exists = True \
            if rdb.db(PROJECT_DB) \
                   .table('riders') \
                   .filter(rdb.row['email'] \
                           .eq(result_json['email'])) \
                   .count().run(rdb_conn) > 0 \
            else False

        check_if_session_exists = True \
            if rdb.db(PROJECT_DB) \
                   .table('sessions') \
                   .filter(rdb.row['email'] \
                           .eq(result_json['email'])) \
                   .count().run(rdb_conn) > 0 \
            else False


api.add_route('/quote/{quote_id}', QuoteResource())
api.add_route('/quote', QuoteResource())
api.add_route('/rider/{rider_id}', RiderResource())
api.add_route('/rider', RiderResource())
api.add_route('/trip/{trip_id}', TripResource())
api.add_route('/trip', TripResource())
api.add_route('/driver', DriverResource())
api.add_route('/driver/location/{driver_id}', DriverResource())











