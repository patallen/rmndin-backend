import datetime
import enum
import bcrypt

from app import db

from app.contacts.vehicles import RedditContactVehicle


class BaseMixin(object):
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    def to_dict(self, exclude=None):
        exclude = exclude or []

        if isinstance(exclude, str):
            exclude = [exclude]

        rv = dict()
        for column in self.__table__.columns:
            name = column.name
            if not name.startswith("_") and name not in exclude:
                value = getattr(self, name)
                if isinstance(value, enum.Enum):
                    value = value.name

                rv[name] = str(value)
        return rv


class DeliveryMethodEnum(enum.Enum):
    reddit = "reddit"
    email = "email"


class Reminder(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(36), nullable=True)
    body = db.Column(db.String)
    eta = db.Column(db.DateTime, nullable=False)
    type_ = db.Column(db.String, nullable=False)
    delivery_method = db.Column(db.Enum(DeliveryMethodEnum), nullable=False)

    fulfilled = db.Column(db.String, nullable=False, default=False)


class User(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    _password = db.Column(db.String, nullable=False)

    reminders = db.relationship('Reminder', backref='user')
    contacts = db.relationship('UserContact', backref='user')

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


class UserContact(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    method = db.Column(db.Enum(DeliveryMethodEnum), nullable=False)
    identifier = db.Column(db.String(256), nullable=False)

    def get_vehicle(self):
        if self.method == DeliveryMethodEnum.reddit:
            veh = RedditContactVehicle(user_contact=self,
                                       verified=self.verified)
        # elif self.method == DeliveryMethodEnum.email:
        #     veh = EmailVehicle(email=self.identifier,
        #                        verified=self.verified)
        else:
            veh = None

        return veh
