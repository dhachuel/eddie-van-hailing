import cloudinary
import cloudinary.uploader
import cloudinary.api
from eddie.db_client import *


IMAGE_URL = 'image_url'


cloudinary.config(
  cloud_name = "dyrjfv6fv",
  api_key = "775455389597988",
  api_secret = "Wjoa4XVYkkksb1mRg_nJrGGhtGg"
)

def save_image(img, user_id):
    response = cloudinary.uploader.upload(img)
    print(response)
    public_id = response['url']
    # Save id to DB
    # Check if rider
    rdb_response = rdb.db('eddie').table('riders').get(user_id).run(rdb_conn)
    if len(rdb_response) > 0:
        rdb.db('eddie').table('riders').get(user_id).update({IMAGE_URL: public_id}).run(rdb_conn)
        return

    # Check if driver
    rdb_response = rdb.db('eddie').table('drivers').get(user_id).run(rdb_conn)
    if len(rdb_response) > 0:
        rdb.db('eddie').table('drivers').get(user_id).update({IMAGE_URL: public_id}).run(rdb_conn)
        return


def load_image(user_id):
    rdb_response = rdb.db('eddie').table('riders').get(user_id).run(rdb_conn)
    if len(rdb_response) > 0:
        return rdb_response[IMAGE_URL]
    else:
        # Check if driver
        rdb_response = rdb.db('eddie').table('drivers').get(user_id).run(rdb_conn)
        if len(rdb_response) > 0:
            return rdb_response[IMAGE_URL]




