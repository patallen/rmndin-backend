import bcrypt
from rmndin import db

from rmndin.lib.db.mixins import BaseMixin
from rmndin.lib.db.enums import DeliveryMethodEnum
from rmndin.lib import vehicles


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    verified = db.Column(db.Boolean, nullable=False, default=False)
    _password = db.Column(db.String, nullable=False)

    reminders = db.relationship('Reminder', backref='user')
    contacts = db.relationship('UserContact', backref='user')

    __repr_columns__ = ["username", "verified"]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt(16))
        return self._password

    @property
    def alias(self):
        return self.first_name or self.username

    def authenticate(self, password):
        pw = password.encode('utf-8')
        hashed = self._password.encode('utf-8')
        return bcrypt.checkpw(pw, hashed)

    @classmethod
    def get_authed_user(cls, username, password):
        user = cls.query.filter(cls.username == username).first()
        if not user:
            return None
        authed = user.authenticate(password)
        if authed:
            return user
        return False

    def owns_contact_ids(self, contact_ids):
        owned_ids = [con.id for con in self.contacts if con.verified]
        return all([c in owned_ids for c in contact_ids])

    def contacts_for_ids(self, contact_ids):
        return [c for c in self.contacts if c.id in contact_ids]


class UserContact(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    method = db.Column(db.Enum(DeliveryMethodEnum), nullable=False)
    identifier = db.Column(db.String(256), nullable=False)

    __repr_columns__ = ['user_id', 'method', 'identifier']

    def get_vehicle(self):
        if self.method == DeliveryMethodEnum.reddit:
            veh = vehicles.RedditContactVehicle(user_contact=self)
        elif self.method == DeliveryMethodEnum.email:
            veh = vehicles.EmailContactVehicle(user_contact=self)
        else:
            veh = None

        return veh
