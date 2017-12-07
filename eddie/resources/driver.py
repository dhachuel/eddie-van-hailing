import requests
from jsonschema import validate, ValidationError
import falcon
from eddie.helpers import getReQLNow
import rethinkdb as rdb
import json
import datetime
from eddie.db_client import *
import hashlib

##
## Driver Resource
##
class DriverResource(object):
    @property
    def __post_request_schema(self):
        return (
            {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"}
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

        # Insert user in database
        check_if_email_exists = True \
            if rdb.db(PROJECT_DB) \
                   .table('drivers') \
                   .filter(rdb.row['email'] \
                           .eq(result_json['email'])) \
                   .count().run(rdb_conn) > 0 \
            else False

        if check_if_email_exists:
            resp.status = falcon.HTTP_303
            resp.body = 'Driver already exists.'
        else:
            rdb_response = rdb.db(PROJECT_DB).table('drivers').insert(
                {
                    "email": result_json['email'],
                    "pwd": hashlib.sha256(str.encode(result_json['password'])).hexdigest(),
                    "username": result_json['username'],
                    "location": {
                        "latitude": None,
                        "longitude": None
                    },
                    "created": getReQLNow()
                }
            ).run(rdb_conn)
            resp.body = json.dumps(
                {
                    "driver_id": rdb_response['generated_keys'][0]
                },
                ensure_ascii=False,
                default=lambda x: x.__str__() if isinstance(x, datetime.datetime) else x
            )
            resp.status = falcon.HTTP_201  # created

    def on_delete(self, req, resp, driver_id):
        """
		Handle user deletion.
		:param req:
		:param resp:
		:return:
		"""
        rdb.db(PROJECT_DB).table('drivers').get(driver_id).delete().run(rdb_conn)
        resp.status = falcon.HTTP_202

    def on_get(self, req, resp):
        email = req.get_param('email') or ''
        password = req.get_param('password') or ''

        pwd_hash = hashlib.sha256(str.encode(password)).hexdigest()

        rdb_response = list(rdb.db(PROJECT_DB) \
            .table('drivers') \
            .filter({
			    "email": email,
			    "pwd": pwd_hash
		    }).pluck('id', 'username').run(rdb_conn))

        if rdb_response is None or len(rdb_response) != 1:
            resp.status = falcon.HTTP_404
        else:
            resp.body = json.dumps(
			    rdb_response[0],
			    ensure_ascii=False,
			    default=lambda x: x.__str__() if isinstance(x, datetime.datetime) else x
		    )
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK


    def on_get(self, req, resp, driver_id):
        rdb_response = list(rdb.db(PROJECT_DB).table('drivers').get(driver_id).pluck('location').run(rdb_conn))

        if rdb_response is None or len(rdb_response) == 0:
            resp.status = falcon.HTTP_404
        else:

            resp.body = json.dumps(
			    rdb_response[0],
			    ensure_ascii=False,
			    default=lambda x: x.__str__() if isinstance(x, datetime.datetime) else x
		    )
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK

    def on_put(self, req, resp, driver_id):
        lat = req.get_param('latitude') or ''
        long = req.get_param('longitude') or ''

        rdb.db(PROJECT_DB).table('drivers').get(driver_id).update(
	        {
		        "location": {
			        "latitude": float(lat),
			        "longitude": float(long)
		        }
	        }
        ).run(rdb_conn)

        resp.status = falcon.HTTP_OK

