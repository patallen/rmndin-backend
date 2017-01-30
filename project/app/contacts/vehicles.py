"""Why the hell do I need a docstring here?."""
import praw
from app import app

reddit = praw.Reddit(user_agent=app.config['REDDIT_USER_AGENT'],
                     client_id=app.config['REDDIT_CLIENT_ID'],
                     client_secret=app.config['REDDIT_SECRET'],
                     username=app.config['REDDIT_USERNAME'],
                     password=app.config['REDDIT_PASSWORD'])


class ContactVehicle(object):
    """Base Vehicle."""

    def __init__(self, identifier, verified):
        """Init."""
        self.identifier = identifier
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
        print "Sending reddit reminder to %s" % self.identifier

    def send_verification(self):
        print "Sending reddit verification to %s!" % self.identifier
