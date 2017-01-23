# from app import db
# from models import Reminder
# from reminders import celery


# @celery.task
# def schedule_reminder(reminder_id):
#     send_reminder(reminder_id)


# def send_reminder(reminder_id):
#     # get the reminder
#     reminder = Reminder.query.get(reminder_id)
#     url = reminder.body
#     user = reminder.user
#     # send_website_email(user)
#     # send email & make sure sent
#     print "Sending email for %s" % url
#     reminder.fulfilled = True
#     db.session.add(reminder)
#     db.session.commit()
