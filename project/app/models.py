import datetime

import bcrypt

from app import db
print db


class BaseMixin(object):
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)


class Reminder(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(36), nullable=True)
    body = db.Column(db.String)
    eta = db.Column(db.DateTime, nullable=False)
    type_ = db.Column(db.String, nullable=False)
    fulfilled = db.Column(db.String, nullable=False, default=False)


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    _password = db.Column(db.String, nullable=False)

    reminders = db.relationship('Reminder', backref='user')


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt(16))
        return self._password
