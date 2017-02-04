from flask import Blueprint, jsonify, request
from flask_jwt import current_identity, jwt_required

from rmndin.users import controllers


usersbp = Blueprint('users', __name__)
verifybp = Blueprint('verify', __name__)


@usersbp.route('/<user_id>/contacts', methods=['POST'])
@jwt_required()
def create_contact(user_id):
    params = request.get_json()
    print current_identity
    rv = controllers.create_user_contact(params, user_id)
    return jsonify(rv)


@usersbp.route('/<user_id>/contacts', methods=['GET'])
@jwt_required()
def get_contacts(user_id):
    rv = controllers.get_contacts(current_identity, user_id)
    return jsonify(rv)


@verifybp.route('/contact/<hashed_key>')
def verify_contact(hashed_key):
    rv = controllers.verify_contact(hashed_key)
    return jsonify(rv)


@verifybp.route('/email/<hashed_key>')
def verify_email(hashed_key):
    rv = controllers.verify_user(hashed_key)
    return jsonify(rv)
