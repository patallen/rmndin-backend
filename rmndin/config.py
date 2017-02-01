from datetime import timedelta

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

if DEBUG:
    JWT_EXPIRATION_DELTA = timedelta(seconds=24 * 60 * 60)

CONTACT_VERIFY_MAX_AGE = 24 * 2 * 60 * 60

URLS = {
    "BASE_URL": 'http://rmndin.dev'
}
