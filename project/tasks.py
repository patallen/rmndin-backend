from celery import Celery
from api import db
celery = Celery('tasks', broker='pyamqp://localhost')


@celery.task
def website_reminder(reminder_id):
    from models import Reminder
    reminder = Reminder.query.get(reminder_id)
    print "Sending reminder for website: %s" % reminder.body
    reminder.fulfilled = True
    db.session.add(reminder)
    db.session.commit()


def cancel_reminder(reminder):
    """Terminate a queued task."""
    task_id = reminder.task_id
    celery.control.revoke([task_id], terminate=True)


def schedule_reminder(reminder):
    func = get_reminder_function(reminder)

    result = func.apply_async(eta=reminder.eta,
                              args=[reminder.id])

    return result


def get_reminder_function(reminder):
    if reminder.type_ == 'website':
        return website_reminder
