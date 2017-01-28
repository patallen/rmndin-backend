from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.views.helpers.users import check_user_param


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
