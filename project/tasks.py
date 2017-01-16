from celery import Celery

celery = Celery('tasks', broker='pyamqp://localhost')


@celery.task
def add(x, y):
    """Add 2 params together."""
    return x + y


def cancel_task(task_id):
    """Terminate a queued task."""
    celery.control.revoke([task_id], terminate=True)
