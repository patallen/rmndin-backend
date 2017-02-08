"""Why the hell do I need a docstring here?."""

from abc import ABCMeta, abstractmethod

import praw
from rmndin import app
from rmndin.lib.verification import contact_verify_url

from rmndin.services.email import send_template_email
from rmndin.auth import validation

reddit = praw.Reddit(user_agent=app.config['REDDIT_USER_AGENT'],
                     client_id=app.config['REDDIT_CLIENT_ID'],
                     client_secret=app.config['REDDIT_SECRET'],
                     username=app.config['REDDIT_USERNAME'],
                     password=app.config['REDDIT_PASSWORD'])


class ContactVehicle(object):
    """Base Vehicle."""

    __metaclass__ = ABCMeta

    def __init__(self, user_contact):
        """Initialize the ContactVehicle."""
        self.contact = user_contact

    def is_valid_identifier(self, identifier):
        if not self.validate_identifier(identifier):
            raise Exception("Invalid Identifier")
        return True

    @abstractmethod
    def validate_identifier(self, identifier):
        """Send the reminder message for the specific service."""
        pass

    @abstractmethod
    def send_reminder(self):
        """Send the reminder message for the specific service."""
        pass

    @abstractmethod
    def send_verification(self):
        """Send the verification link for the DeliveryType service."""
        pass

    @property
    def identifier(self):
        """Shortcut for getting the contact's identifier."""
        return self.contact.identifier

    @property
    def user(self):
        """Return the user associated with the contact."""
        return self.contact.user

    @property
    def user_verified(self):
        """Return the value of User.verified."""
        return self.user.verified

    @property
    def contact_verified(self):
        """Return the value of UserContact.verified."""
        return self.contact.verified

    @property
    def db(self):
        return self.contact.db


class RedditContactVehicle(ContactVehicle):
    """Reddit Vehicle."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the Reddit Vehicle.

        :param contact: - name of user on reddit.
        :param verified: <bool> If the user has been verified.
        """
        super(RedditContactVehicle, self).__init__(*args, **kwargs)
        self.client = reddit

    def validate_identifier(self, identifier):
        return validation.validate_reddit_username(identifier)

    def send_and_save_contact(self):
        try:
            self.is_valid_identifier(self.identifier)
            self.db.session.add(self.contact)
            self.db.session.flush()
            self.send_verification()
            self.db.session.commit()
        except Exception as e:
            print e
            self.db.session.rollback()
            return False, "Reddit username is invalid or does not exist."

        return True, None

    def send_reminder(self, url):
        """Send a reminder via reddit messaging."""
        redditor = praw.models.Redditor(self.client, name=self.identifier)
        redditor.message("Reminder from Rmnd.in!", url)

    def send_verification(self):
        """Send verification email to the UserContact's reddit inbox."""
        secret_key = app.config['CONTACT_VERIFY_SECRET']
        base_url = app.config['URLS']['BASE_URL']
        redditor = praw.models.Redditor(self.client, name=self.identifier)
        verify_url = contact_verify_url(self.contact.id, base_url, secret_key)
        redditor.message("Verify your username!", verify_url)


class EmailContactVehicle(ContactVehicle):
    """Email Vehicle."""

    validation_function = validation.validate_email

    def __init__(self, *args, **kwargs):
        """
        Initialize the EmailContactVehicle.

        :param identifier: <UserContact>

        """
        super(EmailContactVehicle, self).__init__(*args, **kwargs)

    def validate_identifier(self, identifier):
        return validation.validate_email(identifier)

    def send_and_save_contact(self):
        try:
            self.is_valid_identifier(self.identifier)
            self.db.session.add(self.contact)
            self.db.session.flush()
            self.send_verification()
            self.db.session.commit()
        except:
            self.db.session.rollback()
            return False, "Email is invalid or was unreachable."

        self.contact.save()
        return True, None

    def send_reminder(self, url):
        """Send a reminder via email."""
        variables = {"url": url, "username": self.contact.user.alias}
        send_template_email(recipients=[self.identifier],
                            subject="Reminder from Rmnd.in!",
                            from_address="reminders@rmnd.in",
                            variables=variables,
                            template="email/reminder_email")

    def send_verification(self):
        """Send verification email to the UserContact's email."""
        secret_key = app.config['CONTACT_VERIFY_SECRET']
        base_url = app.config['URLS']['BASE_URL']
        verify_url = contact_verify_url(self.contact.id, base_url, secret_key)
        variables = {
            "username": self.contact.user.username,
            "verify_link": verify_url
        }
        send_template_email(recipients=[self.identifier],
                            subject="Verify your Rmnd.in Contact",
                            from_address="accounts@rmnd.in",
                            variables=variables,
                            template="email/verify_contact_email")
