import time
import datetime

from flask import Blueprint, request, jsonify

from app import db
import models
from app.reminders.helpers import schedule_reminder

publicbp = Blueprint('public', __name__)


@publicbp.route('/add_reminder', methods=['POST'])
def add_reminder():
    params = request.get_json()
    url = params.get('url')
    countdown = params.get('countdown')
    eta = datetime.datetime.fromtimestamp(time.time() + countdown)
    type_ = 'website'
    delivery_method = params.get('delivery_method')
    print "Delivery Method: %s" % delivery_method
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
