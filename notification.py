from twilio.rest import Client
from dotenv import load_dotenv
import os
import vonage

load_dotenv()

sender_number = os.getenv("SENDER_NUMBER")
reciever_number = os.getenv("RECEIVER_NUMBER")

def make_phone_call():
    # Initialize the Vonage client with your API credentials
    client = vonage.Client(key='YOUR_API_KEY', secret='YOUR_API_SECRET')
    voice = vonage.Voice(client)

    # Define the call parameters
    response = voice.create_call({
        'to': [{'type': 'phone', 'number': 'RECIPIENT_PHONE_NUMBER'}],
        'from': {'type': 'phone', 'number': 'YOUR_VONAGE_NUMBER'},
        'answer_url': ['https://nexmo-community.github.io/ncco-examples/first_call_talk.json']
    })

    print(response)


def twilio_authentication() -> Client:
    # Twilio account credeNtials
    account_sid = os.getenv("TWILIO_ID")
    auth_token = os.getenv("TWILIO_TOKEN")
    client = Client(account_sid, auth_token)
    return client
    
# Function to send a WhatsApp message using Twilio
def send_sms() -> None:
    client = twilio_authentication()
    # Send WhatsApp message
    message = client.messages.create(
        body="Alert: Unauthorized access detected in your car!",
        from_= f'{sender_number}',  # Twilio sandbox number
        to= f"{reciever_number}"     # Replace with your number
    )

    print("WhatsApp message sent. SID:", message.sid)
    
    
def make_call() -> None:
    client = twilio_authentication()
    # Send WhatsApp message
    call = client.calls.create(
        twiml="<Response><Say> Unauthorized access detected in your car!</Say></Response>",
        from_= sender_number,  # Twilio sandbox number
        to= reciever_number    # Replace with your number
    )
    print("WhatsApp message sent. SID:", call.sid)
