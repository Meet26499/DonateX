from twilio.rest import Client
from django.conf import settings

# Function to send otp using Twilio
def send_otp(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    print(settings.TWILIO_PHONE_NUMBER, 'settings.TWILIO_PHONE_NUMBER')
    print(phone_number, 'phone_number')

    message = client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f'Your OTP code for DonateX is: {otp_code}'
    )

    return message.sid