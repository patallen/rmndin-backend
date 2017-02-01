import re

from rmndin import app, db
from rmndin.users.models import User, UserContact
from rmndin.lib.verification import deserialize_key


def _check_username(username):
    if not username or len(username) < 3:
        return False, "must be at least 3 characters in length"

    valid = re.match('^[\w-]+$', username) is not None
    if not valid:
        return False, "must only contain letters and numbers"

    query = db.session.query(User.id)
    filtered = query.filter(User.username.ilike(username))
    existing = filtered.count()

    if existing:
        return False, "already taken"

    return (True, None)


def _check_password(password):
    if not password or len(password) < 8:
        return False, "must be at least 8 characters in length"

    digit_re = re.compile(r'[0-9]')
    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    for regex in (digit_re, upper_re, lower_re):
        valid = regex.search(password) is not None
        if not valid:
            return False, "must contain uppercase, lowercase, and a digit"

    return (True, None)


def _check_email(email):
    test = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    valid = re.match(test, email) is not None

    if not valid:
        return False, "not valid"

    query = db.session.query(User.id)
    filtered = query.filter(User.email.ilike(email))
    existing = filtered.count()

    if existing:
        return False, "already in use"

    return (True, None)


def check_user_param(param, value):
    rv = None

    if param == 'username':
        rv = _check_username(value)
    elif param == 'password':
        rv = _check_password(value)
    elif param == 'email':
        rv = _check_email(value)
    else:
        raise Exception("Invalid parameter name: %s" % param)

    return rv


def verify_user(hashed_key):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    max_age = app.config['CONTACT_VERIFY_MAX_AGE']
    try:
        info = deserialize_key(hashed_key, secret_key, max_age)
    except Exception as e:
        print(e)
        return False, "invalid key"

    email = info.get('email')
    user = User.query.filter_by(email=email).first()

    if user and user.verified:
        return False, "already verified"
    elif user and not user.verified:
        user.verified = True
        contact = UserContact(method='email', identifier=email, verified=True)
        db.session.add(user, contact)
        db.session.commit()
        return True, None
    else:
        return False, "invalid key"
