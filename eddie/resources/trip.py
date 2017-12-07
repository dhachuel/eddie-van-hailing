import requests
from jsonschema import validate, ValidationError
import msgpack
from geopy.geocoders import Nominatim
import falcon
from eddie.helpers import getReQLNow
import rethinkdb as rdb
import json
import datetime
from eddie.send_sms import send_message
from eddie.db_client import *
import logging

##
## Trip Resource
##
class TripResource(object):

    @property
    def __post_request_schema(self):
        return (
            {
                "type": "object",
                "properties": {
                    "quote_id": {"type": "string"},
                    "vehicle_type": {"type": "string"}
                }
            }
        )

    @property
    def __put_request_schema(self, reqp, resp, trip_id):
        return (
            {
                "type": "object",
                "properties": {
                    "vehicle_type": {"type": "string"}
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

        # Get quote
        quote = rdb.db(PROJECT_DB).table('quotes').get(result_json['quote_id']).run(rdb_conn)

        if quote is None or len(quote) == 0:
            raise falcon.HTTPError(
                falcon.HTTP_404,
                'Error in Quote',
                'Wrong quote ID.'
            )


        # Insert trip in database
        new_trip = {
            "rider_id": quote['rider_id'],
            "pickup_location": quote["pickup_location"],
            "dropoff_location": quote["dropoff_location"],
            "vehicle_type": result_json['vehicle_type'],
            "price": quote['quote'][result_json['vehicle_type']],
            "driver_id": None,
            "status": "OPEN",
            "created": getReQLNow()
        }
        rdb_response = rdb.db(PROJECT_DB).table('trips').insert(
            new_trip
        ).run(rdb_conn)
        trip_id = rdb_response['generated_keys'][0]

        self.send_numbers()

        resp.body = json.dumps(
            {"trip_id": trip_id},
            ensure_ascii = False,
            default = lambda x: x.__str__() if isinstance(x, datetime.datetime) else x
        )
        resp.status = falcon.HTTP_201 # created


    def send_numbers(self):
        cursor = rdb.db(PROJECT_DB).table("drivers").run(rdb_conn)
        for document in cursor:
            if 'phone_number' in document:
                send_message(document['phone_number'])


    def on_get(self, req, resp, trip_id):
        rdb_response = rdb.db(PROJECT_DB).table('trips').get(trip_id).run(rdb_conn)

        if rdb_response is None or len(rdb_response) == 0:
            resp.status = falcon.HTTP_404
        else:

            resp.body = json.dumps(
                rdb_response,
                ensure_ascii=False,
                default=lambda x: x.__str__() if isinstance(x, datetime.datetime) else x
            )
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
