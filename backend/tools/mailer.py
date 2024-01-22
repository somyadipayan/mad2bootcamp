from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def init_app(app):
    mail.init_app(app)

def send_email_text(to, subject, body):
    sender = 'admin@ticketshow.com'
    with current_app.app_context():
        message = Message(sender=sender, subject=subject, recipients=[to], body=body)
        mail.send(message)

def send_email_html(to, subject, html):
    sender = 'admin@ticketshow.com'
    with current_app.app_context():
        message = Message(sender=sender, subject=subject, recipients=[to], html=html)
        mail.send(message)