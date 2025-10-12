account_sid = "AC55d3b47be0db93c9d4766addb786b2b3"
auth_token = "3c7e4400ed2e9675e628e49c44738db0"
twilio_phone_number = "+18555785234"  # Your Twilio phone number
  # The phone number to call
import os
from twilio.rest import Client
client = Client(account_sid, auth_token)

def make_call(to_phone_number):
    """Makes a call to the specified phone number using Twilio."""
    try:
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",  # URL for TwiML instructions
            to=to_phone_number,
            from_=twilio_phone_number
        )
        print(f"Call initiated successfully. Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make call: {e}")