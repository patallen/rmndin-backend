import time
import datetime

from flask import Blueprint, request, jsonify

from rmndin import db
from rmndin.reminders import models
from rmndin.reminders.helpers import schedule_reminder

reminders = Blueprint('reminders', __name__)


@reminders.route('/add', methods=['POST'])
def add_reminder():
    params = request.get_json()
    url = params.get('url')
    countdown = params.get('countdown')
    eta = datetime.datetime.fromtimestamp(time.time() + countdown)
    type_ = 'website'
    delivery_method = params.get('delivery_method')

    reminder = models.Reminder(body=url,
                               type_=type_,
                               eta=eta,
                               delivery_method=delivery_method)

    db.session.add(reminder)
    db.session.flush()

    result = schedule_reminder(reminder)

    reminder.task_id = result.id
    db.session.commit()

    return jsonify(reminder.to_dict())