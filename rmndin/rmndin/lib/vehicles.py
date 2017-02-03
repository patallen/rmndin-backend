"""Why the hell do I need a docstring here?."""
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

    def __init__(self, user_contact, verified):
        """Init."""
        self.contact = user_contact
        self.verified = verified
        self.client = None
        pass

    def send_reminder(self):
        """Send the message to the proper user."""
        pass

    def send_verification(self):
        pass


class RedditContactVehicle(ContactVehicle):
    """Reddit Vehicle."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the Reddit Vehicle.

        :identifier - name of user on reddit.
        """
        super(RedditContactVehicle, self).__init__(*args, **kwargs)
        self.client = reddit

    def send_reminder(self, message):
        """
        Sends
        """
        print "Sending reddit reminder to %s" % self.contact.identifier

    def send_verification(self):
        """Send verification email to the UserContact's reddit inbox."""
        secret_key = app.config['CONTACT_VERIFY_SECRET']
        base_url = app.config['URLS']['BASE_URL']
        redditor = praw.models.Redditor(self.client,
                                        name=self.contact.identifier)
        verify_url = contact_verify_url(self.contact.id, base_url, secret_key)
        redditor.message("Verify your username!", verify_url)


class EmailContactVehicle(ContactVehicle):
    """Email Vehicle."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the Email Vehicle.

        :param identifier: <str> Email address for UserContact.
        :param verified: <bool> If the user has been verified.
        """
        super(EmailContactVehicle, self).__init__(*args, **kwargs)

    def send_reminder(self, message):
        """
        Sends
        """
        print "Sending reddit reminder to %s" % self.contact.identifier

    def send_verification(self):
        """Send verification email to the UserContact's email."""
        secret_key = app.config['CONTACT_VERIFY_SECRET']
        base_url = app.config['URLS']['BASE_URL']
        verify_url = contact_verify_url(self.contact.id, base_url, secret_key)
        variables = {
            "username": self.contact.user.username,
            "verify_link": verify_url
        }
        send_template_email(recipients=[self.contact.identifier],
                            subject="Verify your Rmnd.in Contact",
                            from_address="accounts@rmnd.in",
                            variables=variables,
                            template="email/verify_contact_email")
