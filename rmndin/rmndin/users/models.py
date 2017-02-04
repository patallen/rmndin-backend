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
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    _password = db.Column(db.String, nullable=False)

    reminders = db.relationship('Reminder', backref='user')
    contacts = db.relationship('UserContact', backref='user')

    __repr_columns__ = ["username", "verified"]

    @property
    def password(self):
        """Return the hashed password we have stored for the user."""
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt(16))
        return self._password

    @property
    def alias(self):
        """What we will call the user."""
        return self.first_name or self.username

    def authenticate(self, password):
        """Check the provided password against the hash we have stored."""
        pw = password.encode('utf-8')
        hashed = self._password.encode('utf-8')
        return bcrypt.checkpw(pw, hashed)

    @classmethod
    def get_authed_user(cls, username, password):
        """Get and authenticate a user given a username and password."""
        user = cls.query.filter(cls.username == username).first()
        if not user:
            return None
        authed = user.authenticate(password)
        if authed:
            return user
        return False

    def owns_contact_ids(self, contact_ids):
        """Verify that all of the contact_ids are owned by this user."""
        owned_ids = [con.id for con in self.contacts if con.verified]
        return all([c in owned_ids for c in contact_ids])

    def contacts_for_ids(self, contact_ids):
        """Get the UserContact instances for any contact_ids that match."""
        return [c for c in self.contacts if c.id in contact_ids]

    def has_access(self, user_id=None):
        """Verify that the user is allowed to access contents of user_id.

        For now this is just checking if the user has the user_id or
        if the user is and admin.
        """
        return self.id == int(user_id) or self.is_admin


class UserContact(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', onupdate="CASCADE", ondelete='CASCADE'),
        nullable=False
    )
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
