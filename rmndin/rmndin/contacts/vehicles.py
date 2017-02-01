"""Why the hell do I need a docstring here?."""
import praw
from rmndin import app
from rmndin.contacts.verification import contact_verify_url

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
        redditor = praw.models.Redditor(self.client,
                                        name=self.contact.identifier)
        url = contact_verify_url(self.contact.id)
        redditor.message("Verify your username!", url)
        print "Sending reddit verification to %s!" % self.contact.identifier
