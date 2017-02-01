import re

from rmndin.users.models import User


def validate_username(username):
    errors = []
    if not username or len(username) < 8:
        errors.append("Username must be at least 8 characters in length.")

    valid = re.match('^[\w-]+$', username) is not None
    if not valid:
        errors.append("Username must only contain letters and numbers.")

    return ((not len(errors)), errors)


def validate_password(password):
    errors = []
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters.")

    digit_re = re.compile(r'[0-9]')
    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    for n, regex in (("number", digit_re),
                     ("uppercase letter", upper_re),
                     ("lowercase letter", lower_re)):

        valid = regex.search(password) is not None
        if not valid:
            interim = "n " if n.startswith("u") else " "
            errors.append("Password must contain a%s %s." % interim, n)

    return ((not len(errors)), errors)


def validate_confirmation_pass(password, password2):
    errors = []
    if password != password2:
        errors = ["Passwords do not match."]
    return ((not len(errors)), errors)


def validate_email(email):
    test = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(test, email) is None:
        return False, ["Not a valid email address."]

    return (True, [])
