from flask import Blueprint, jsonify, request
from flask_jwt import current_identity, jwt_required

from rmndin import app, db
from rmndin.users.models import User
from rmndin.views.helpers.users import check_user_param
from rmndin.views.helpers.contacts import create_contact
from rmndin.lib.verification import email_verify_url

from rmndin.views import helpers


users = Blueprint('users', __name__)
verify = Blueprint('verify', __name__)


def send_email_verification(email):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    base_url = app.config['URLS']['BASE_URL']
    print email_verify_url(email, base_url, secret_key)


@users.route('/create', methods=["POST"])
def create_user():
    params = request.get_json()
    check = ["username", "password", "email", "confirm"]

    errors_by_param = {}
    for param in check:
        value = params.get(param)
        if value is None:
            errors_by_param[param] = "cannot not be blank"
        elif param == "confirm":
            if params.get('confirm') != params.get('password'):
                errors_by_param[param] = "does not match"
        else:
            valid, error = check_user_param(param, value)
            if not valid:
                errors_by_param[param] = error

    if len(errors_by_param):
        print len(errors_by_param)
        return jsonify(errors_by_param)

    first_name = params.get('first_name')
    last_name = params.get('last_name')

    user = User(username=params.get('username'),
                password=params.get('password').encode('utf-8'),
                email=params.get('email'),
                first_name=first_name,
                last_name=last_name)

    db.session.add(user)
    db.session.commit()
    send_email_verification(email=user.email)
    return jsonify(user.to_dict())


@users.route('/contacts', methods=['POST'])
@jwt_required()
def create_user_contact():
    params = request.get_json()
    identifier = params.get('identifier')
    method = params.get('method')
    print "Creating contact..."
    val, result = create_contact(current_identity.id, method, identifier)
    print val, result
    return jsonify(result)


@users.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user = current_identity
    contacts = [u.to_dict() for u in user.contacts if u.verified]
    return jsonify(contacts)


@verify.route('/contact/<hashed_key>')
def verify_contact(hashed_key):
    contact = helpers.contacts.verify_contact(hashed_key)
    if not contact:
        return "Invalid verification link."
    return jsonify(contact.to_dict())


@verify.route('/email/<hashed_key>')
def verify_email(hashed_key):
    user, code = helpers.users.verify_user(hashed_key)
    if not user:
        msg = "Could not verify due to %s." % code
    else:
        msg = "Success! Please log in :)"
    return jsonify(msg)
