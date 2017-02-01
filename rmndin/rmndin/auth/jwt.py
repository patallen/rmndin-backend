from rmndin.users.models import User


def authenticate(username, password):
    return User.get_authed_user(username, password)


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)
