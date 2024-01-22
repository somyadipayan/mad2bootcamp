from .workers import celery
from models import User, Theatre, Shows, TransactionTable, db
from datetime import datetime
from .mailer import send_email_html, send_email_text
from celery.schedules import crontab
from flask import render_template


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30 ,monthly_reminder.s(), name='Every 30 Seconds')
    #sender.add_periodic_task(crontab(hour = 10, minute = 0), daily_reminder.s(), name='Everyday at 10 AM')
    #sender.add_periodic_task(crontab(hour = 0, minute = 0, day_of_month=1), monthly_reminder.s(), name='Every month at 00:00')


@celery.task
def add():
    a=1
    b=2
    return (a+b)

@celery.task
def test(to):
    send_email_text(to=to,subject='Test', body='Test')
    return "success"

@celery.task
def daily_reminder():
    send_email_text(to='x@y.com',subject='Test', body='Test')
    return "success"

@celery.task
def monthly_reminder():
    username = "Somya"
    total = 1800
    booking_details = [{'movie':'Harry Potter','theatre':'Inox','ticket_count':2,'total_amount':600},
                      {'movie':'Star Wars','theatre':'PVR','ticket_count':4,'total_amount':1000},
                      {'movie':'WAR MOVIE','theatre':'PVR','ticket_count':1,'total_amount':200},
                      ]
    html_content = render_template('monthly_report.html', username = username, total=total, booking_details= booking_details)
    
    send_email_html(to='users@gmail.com',subject='Your Monthly Report', html=html_content)
    return "success"
