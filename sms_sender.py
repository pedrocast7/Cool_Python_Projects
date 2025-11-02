from twilio.rest import Client
account_sid = 'acc_sid'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)
message = client.messages.create(
    from_='+your_twilio_number',
    to='+verified_number',
    body='Hello, I\'m sending this message using Python! How cool is that?'
)
print(message.sid)