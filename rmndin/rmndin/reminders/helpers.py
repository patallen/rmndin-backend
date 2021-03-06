from rmndin import db
from rmndin.reminders import celery

import rmndin.tasks


def cancel_reminder(reminder):
    """Terminate a queued task."""
    task_id = reminder.task_id
    celery.control.revoke([task_id], terminate=True)
    reminder.task_id = None
    db.session.add(reminder)
    db.session.commit()


def schedule_reminder(reminder):
    """Simple helper to queue a reminder in celery."""
    result = rmndin.tasks.schedule_reminder.apply_async(
        eta=reminder.eta,
        args=[reminder.id]
    )

    return result
