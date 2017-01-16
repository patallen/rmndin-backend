from celery import Celery

celery = Celery('tasks', broker='pyamqp://localhost')


@celery.task
def schedule_reminder(reminder):
    """Add 2 kwargs together."""
    func = get_reminder_function(reminder)
    kwargs = get_reminder_kwargs(reminder)
    eta = get_reminder_eta(reminder)

    result = func.apply_async(eta, kwargs=kwargs)

    return result


def cancel_reminder(reminder):
    """Terminate a queued task."""
    task_id = reminder.task_id
    celery.control.revoke([task_id], terminate=True)
