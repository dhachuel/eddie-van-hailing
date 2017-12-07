import sys, os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__location__))
print(os.path.dirname(__location__))
import falcon
from falcon import testing
import pytest
import datetime

from eddie.app import api
from eddie.helpers import logisticMap, getReQLNow


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_helpers():
    assert getReQLNow().date() == datetime.datetime.now().date()



# def test_get_quote(client):
#     doc = {
#         "created": "2017-12-07 03:19:32.014000+00:00",
#         "dropoff_location": {
#             "latitude": 40.759155474313346,
#             "longitude": -73.95326614379883
#         },
#         "id": "a825b041-ed6b-4b66-a96d-dcfdb1488a89",
#         "pickup_datetime": "2017-11-16 15:42:49.440762-05:00",
#         "pickup_location": {
#             "latitude": 40.7246704,
#             "longitude": -73.9918311
#         },
#         "quote": {
#             "double-necker": 46.82,
#             "kramer": 34.71,
#             "ukelele": 18.72
#         },
#         "rider_id": "58d7875b-40f1-4cab-b650-bfc972bb8a46"
#     }
#
#     response = client.simulate_get('/quotes/a825b041-ed6b-4b66-a96d-dcfdb1488a89')
#     result_doc = response.content
#
#
#     assert result_doc == doc
#     assert response.status == falcon.HTTP_OK