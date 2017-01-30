from flask import Blueprint, jsonify, request
from flask_jwt import current_identity, jwt_required

from app import db
from app.models import User
from app.views.helpers.users import check_user_param
from app.contacts import verification


users = Blueprint('users', __name__)


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

    return jsonify(user.to_dict())


@users.route('/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    params = request.get_json()
    identifier = params.get('identifier')
    method = params.get('method')
    print "Creating contact..."
    val, result = verification.create_contact(current_identity.id, method, identifier)
    print val, result
    return jsonify(result)

    contact = UserContact(method=method,
                          identifier=identifier,
                          user_id=user.id)
    db.session.add(contact)
    db.session.commit()
    pprint(user.contacts)
    return jsonify(contact.to_dict())