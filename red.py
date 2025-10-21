account_sid = "TWILIO_SID"
auth_token = "TWILIO_AUTH_TOKEN"
twilio_phone_number = "TWILIO_NUMBER"  # Your Twilio phone number
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
