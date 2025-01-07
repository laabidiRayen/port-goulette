from flask_mail import Message
from extensions import mail

def send_email(recipient, subject, body):
    try:
        msg = Message(subject, recipients=[recipient], body=body)
        print(mail)
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")