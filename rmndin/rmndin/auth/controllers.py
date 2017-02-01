from rmndin import app
from rmndin.auth.validation import (
    validate_username,
    validate_password,
    validate_confirmation_pass,
    validate_email,
)
from rmndin.lib.verification import email_verify_url
from rmndin.users.models import User


def user_registration(params):
    username = params.get("username")
    password = params.get("password")
    password2 = params.get("confirm")
    email = params.get("email")

    if not all((username, password, password2, email)):
        return {"error": "All fields required."}

    errors_by_param = {}
    check, username_errors = validate_username(username)
    if not check:
        errors_by_param['username'] = username_errors

    check, password_errors = validate_password(password)
    if not check:
        errors_by_param['password'] = password_errors

    check, email_errors = validate_email(email)

    if not check:
        errors_by_param['email'] = email_errors

    check, confirm_errors = validate_confirmation_pass(password, password2)
    if not check:
        errors_by_param['confirm'] = confirm_errors

    if User.exists_by_key('username', value=username, case_sensitive=False):
        errors_by_param['username'] = ["Username is not available."]

    if User.exists_by_key('email', value=email, case_sensitive=False):
        errors_by_param['email'] = ["Email address is not available."]

    if len(errors_by_param):
        return {"error": errors_by_param}

    first_name = params.get('first_name')
    last_name = params.get('last_name')

    user = User.create(username=params.get('username'),
                       password=params.get('password').encode('utf-8'),
                       email=params.get('email'), first_name=first_name,
                       last_name=last_name)

    _send_email_verification(email=user.email)

    return {"success": user.to_dict()}


def _send_email_verification(email):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    base_url = app.config['URLS']['BASE_URL']
    url = email_verify_url(email, base_url, secret_key)
    print url
