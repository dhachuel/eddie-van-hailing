import sys, os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__location__))
print(os.path.dirname(__location__))
from falcon import testing
import pytest
import datetime
from eddie.app import api
from eddie.helpers import logisticMap, getReQLNow
import eddie.middleware
from eddie.db_client import rdb_conn, rdb, dbSetup, PROJECT_DB


# dbSetup(PROJECT_DB, ['test'])
global gen_id
gen_id = None

@pytest.fixture
def client():

    return testing.TestClient(api)


def test_helpers():
    assert getReQLNow().date() == datetime.datetime.now().date()

def test_insert_and_delete_user():
    """
    Test if adding a rider to the db is successful
    """
    global gen_id
    test_result = True
    message = "Insert test successful"
    name = "Testing name, this will not be a user name. we will check for injections"
    try:
        response = rdb.db('eddie').table('riders').insert({'name': name}).run(rdb_conn)
        if len(response['generated_keys']) == 0:
            test_result = False
            message = "Rider not added to the DB"
        else:
            gen_id = response['generated_keys'][0]

    except:
        print("error")
        test_result = False
        message = "error connecting to the DB"
    finally:
        print(message)
        assert test_result

def test_middleware_user_validation():
    """
    Test if middle ware approves a user with a valid id
    :return:
    """
    assert eddie.middleware.AuthMiddleware().is_user_valid(gen_id)


def test_deletion():
    """
    Test if adding a rider to the db is successful
    """
    response = rdb.db('eddie').table('riders').get(gen_id).delete().run(rdb_conn)
    if response['deleted'] == 0:
        assert False





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