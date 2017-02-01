from flask import Blueprint, jsonify, request
from flask_jwt import current_identity, jwt_required

from rmndin.users import controllers


users = Blueprint('users', __name__)
verify = Blueprint('verify', __name__)


@users.route('/contacts', methods=['POST'])
@jwt_required()
def create_user_contact():
    params = request.get_json()
    rv = controllers.create_user_contact(params)
    return jsonify(rv)


@users.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user = current_identity
    contacts = [u.to_dict() for u in user.contacts if u.verified]
    return jsonify(contacts)


@verify.route('/contact/<hashed_key>')
def verify_contact(hashed_key):
    rv = controllers.verify_contact(hashed_key)
    return jsonify(rv)


@verify.route('/email/<hashed_key>')
def verify_email(hashed_key):
    rv = controllers.verify_user(hashed_key)
    return jsonify(rv)
