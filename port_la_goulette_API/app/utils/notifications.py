from flask_mail import Message
from extensions import mail

def send_email(recipient, subject, body):
    try:
        if isinstance(recipient, list):
            recipients = recipient
        else:
            recipients = [recipient]
        # Ensure body is a string
        if not isinstance(body, str):
            body = str(body)
        # Debugging: Print the recipients list
        print(f"Recipients list: {recipients}")
        
        msg = Message(subject, recipients=recipients, body=body)
        # Debugging: Print the message object
        print(f"Message object: {msg}")
        print(f"Recipients: {msg.recipients}")
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")