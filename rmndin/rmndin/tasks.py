from rmndin.reminders.models import Reminder
from rmndin.reminders import celery
import traceback

@celery.task
def schedule_reminder(reminder_id):
    send_reminder(reminder_id)


def send_reminder(reminder_id):
    # get the reminder
    reminder = Reminder.query.get(reminder_id)

    contact_vehicles = []
    for contact in reminder.user.contacts:
        contact_vehicles.append(contact.get_vehicle())

    errors = []
    for vehicle in contact_vehicles:
        try:
            vehicle.send_reminder(reminder.url)
        except Exception as e:
            print(e)
            errors.append(
                "Reminder: %s - UserContact: %s" % (reminder.id, contact.id)
            )
            traceback.print_exc()

    if len(errors):
        # send email to developer for now.
        # should eventual log to some sort of admin panel
        # we could schedule it to try again in x min/hour
        import pprint
        pprint.pprint(errors)
        pass

    reminder.fulfilled = True
    reminder.task_id = None
    reminder.save()
