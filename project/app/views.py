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

    reminder = models.Reminder(body=url, type_=type_, eta=eta)

    db.session.add(reminder)
    db.session.flush()

    result = schedule_reminder(reminder)

    reminder.task_id = result.id
    db.session.commit()
    # Create reminder
    # Schedule reminder in celery & set task_id in DB
    # Commit reminder
    # Return reminder JSON
    rv = reminder.to_dict()
    return jsonify(rv)
