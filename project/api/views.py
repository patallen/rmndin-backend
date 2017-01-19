import time, datetime

from flask import request, jsonify


import models
from api import app, db
import tasks


@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    params = request.get_json()
    url = params.get('url')
    countdown = params.get('countdown')
    eta = datetime.datetime.fromtimestamp(time.time() + countdown)
    type_ = 'website'

    reminder = models.Reminder(body=url, type_=type_, eta=eta)

    db.session.add(reminder)
    db.session.flush()

    result = tasks.schedule_reminder(reminder)

    reminder.task_id = result.id
    db.session.commit()
    # Create reminder
    # Schedule reminder in celery & set task_id in DB
    # Commit reminder
    # Return reminder JSON
    rv = reminder.__dict__
    rv.pop('_sa_instance_state')
    return jsonify(rv)
