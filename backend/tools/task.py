from .workers import celery
from models import User, Theatre, Shows, TransactionTable, db
from datetime import datetime
from .mailer import send_email
from celery.schedules import crontab


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(30, daily_reminder.s(), name='Every 30 Seconds')
    sender.add_periodic_task(crontab(hour = 10, minute = 0), daily_reminder.s(), name='Everyday at 10 AM')
    sender.add_periodic_task(crontab(hour = 0, minute = 0, day_of_month=1), monthly_reminder.s(), name='Every month at 00:00')


@celery.task
def add():
    a=1
    b=2
    return (a+b)

@celery.task
def test(to):
    send_email(to=to,subject='Test', body='Test')
    return "success"

@celery.task
def daily_reminder():
    send_email(to='users@gmail.com',subject='Test', body='Test')
    return "success"

@celery.task
def monthly_reminder():
    send_email(to='users@gmail.com',subject='Test', body='Test')
    return "success"