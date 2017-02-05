from flask import Blueprint, jsonify, request
from rmndin.auth.decorators import require_user_access
from rmndin.users import controllers


usersbp = Blueprint('users', __name__)
verifybp = Blueprint('verify', __name__)


@usersbp.route('/<user_id>/contacts', methods=['POST'])
@require_user_access
def create_contact(user_id):
    params = request.get_json()
    rv = controllers.create_user_contact(params, user_id)
    return jsonify(rv)


@usersbp.route('/<user_id>/contacts', methods=['GET'])
@require_user_access
def get_contacts(user_id):
    rv = controllers.get_contacts(user_id)
    return jsonify(rv)


@verifybp.route('/contact/<hashed_key>')
@require_user_access
def verify_contact(hashed_key):
    rv = controllers.verify_contact(hashed_key)
    return jsonify(rv)


@verifybp.route('/email/<hashed_key>')
@require_user_access
def verify_email(hashed_key):
    rv = controllers.verify_user(hashed_key)
    return jsonify(rv)
