from rmndin import db
from rmndin.reminders.models import Reminder
from rmndin.reminders import celery


@celery.task
def schedule_reminder(reminder_id):
    send_reminder(reminder_id)


def send_reminder(reminder_id):
    # get the reminder
    reminder = Reminder.query.get(reminder_id)
    url = reminder.url
    user = reminder.user
    created = reminder.created
    # send_website_email(user)
    # send email & make sure sent
    print "Sending email for %s" % url
    reminder.fulfilled = True
    reminder.save()
