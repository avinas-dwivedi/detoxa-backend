def whatsapp_notification(mobile_no, msg_body):
    import os
    from twilio.rest import Client
    sid = 'AC3d28da5c300e373fa7e2bf1c201db414'
    authToken = '008c71137a31da79f4be26c96474ed09'
    client = Client(sid, authToken)
    to_whatsapp_no = ''
    if len(mobile_no) == 10:
        to_whatsapp_no = 'whatsapp:+91' + mobile_no
    else:
        to_whatsapp_no = 'whatsapp:+' + mobile_no
    msg_body = msg_body
    message = client.messages.create(from_='whatsapp:+14155238886', body=msg_body, to=to_whatsapp_no)
    print(message.sid)

