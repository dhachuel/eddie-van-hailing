# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC1ac396cfdb8e97412811b147e91e8126"
auth_token = "dac7e7a5eda2fdafc5e7d2f2405e8fc0"


def send_message(phone_number):
    client = Client(account_sid, auth_token)
    number = "+12138057136" # Free number from twilio
    client.api.account.messages.create(
        to=phone_number,
        from_=number,
        body="You have a ride request!!\nGo to the Eddie-Van-Hailing app to see it")



