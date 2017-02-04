"""Why the hell do I need a docstring here?."""

from abc import ABCMeta, abstractmethod

import praw
from rmndin import app
from rmndin.lib.verification import contact_verify_url

from rmndin.services.email import send_template_email


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

    def send_reminder(self, message):
        """Send a reminder via reddit messaging."""
        print "Sending reddit reminder to %s" % self.identifier

    def send_verification(self):
        """Send verification email to the UserContact's reddit inbox."""
        secret_key = app.config['CONTACT_VERIFY_SECRET']
        base_url = app.config['URLS']['BASE_URL']
        redditor = praw.models.Redditor(self.client,
                                        name=self.identifier)
        verify_url = contact_verify_url(self.contact.id, base_url, secret_key)
        redditor.message("Verify your username!", verify_url)


class EmailContactVehicle(ContactVehicle):
    """Email Vehicle."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the EmailContactVehicle.

        :param identifier: <UserContact>

        """
        super(EmailContactVehicle, self).__init__(*args, **kwargs)

    def send_reminder(self, message):
        """Send a reminder via email."""
        print "Sending reddit reminder to %s" % self.identifier

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
