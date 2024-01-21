from .workers import celery
from models import User, Theatre, Shows, TransactionTable, db
from datetime import datetime
from .mailer import send_email



@celery.task
def add():
    a=1
    b=2
    return (a+b)

@celery.task
def test(to):
    send_email(to=to,subject='Test', body='Test')
    return "success"