import datetime

from api import db


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String)
    eta = db.Column(db.DateTime, nullable=False)
    type_ = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
