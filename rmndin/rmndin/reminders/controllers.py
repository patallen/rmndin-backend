
import datetime
from rmndin import app
import dateutils
from flask_jwt import current_identity

from rmndin.lib import formats
from rmndin.reminders.models import Reminder
from rmndin.reminders.helpers import schedule_reminder
from rmndin.users.models import User


def add_reminder(params, user_id):
    allowed = current_identity.has_access(user_id)
    if not allowed:
        return {"error": "Access denied."}

    if user_id == current_identity.id:
        user = current_identity
    else:
        user = User.query.get(user_id)

    eta = _eta_from_params(params)
    url = params.get('url')
    contact_ids = params.get('contacts', [])
    user_id = user.id
    ensured = user.owns_contact_ids(contact_ids)

    if not _valid_horizon(eta):
        return {"error": "Reminder must be at least an hour from now."}
    elif not ensured:
        return {"error":
                "You must own these contacts, and they must be verifed."}

    rem = Reminder.create(user_id=user_id, url=url, eta=eta, commit=False)
    contacts = user.contacts_for_ids(contact_ids)
    rem.add_contacts(contacts, commit=True)
    rem.task_id = schedule_reminder(rem).id
    rem.save()
    return {"success": rem.to_dict(include_contacts=True)}


def _valid_horizon(eta):
    if app.config.get('DEBUG'):
        return True
    time_delta = eta - datetime.now()
    if time_delta.seconds < 60 * 60:
        return False
    return True


def _eta_from_params(params):
    set_date = params.get('set_date', None)

    if set_date:
        rv = formats.convert_utc_datetime(set_date)
    else:
        countdown = params.get('countdown') or {}
        hours = countdown.get('hours') or 0
        days = countdown.get('days') or 0
        weeks = countdown.get('weeks') or 0
        months = countdown.get('months') or 0
        delta = dateutils.relativedelta(hours=hours, days=days,
                                        weeks=weeks, months=months)
        today = datetime.datetime.now()
        rv = today + delta

    return rv
