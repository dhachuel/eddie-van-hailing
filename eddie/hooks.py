from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time

import falcon


def api_key(req, resp, resource, params):

    key = req.get_param('api_key')
    if key is None:
        raise falcon.HTTPForbidden(
            description='API KEY is required')


def log_operation(req, resp, resource):
	logging.info('Request at ' + str(time.time()) + ' and token=' + req.params.get('Authorization'))