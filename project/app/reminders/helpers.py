# from reminders import celery

# import reminders.tasks


# def cancel_reminder(reminder):
#     """Terminate a queued task."""
#     task_id = reminder.task_id
#     celery.control.revoke([task_id], terminate=True)


# def schedule_reminder(reminder):
#     result = reminders.tasks.schedule_reminder.apply_async(
#         eta=reminder.eta,
#         args=[reminder.id]
#     )

#     return result
