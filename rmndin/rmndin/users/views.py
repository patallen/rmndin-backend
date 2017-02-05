from flask import Blueprint, request

from rmndin.auth.decorators import require_user_access
from rmndin.lib.decorators import require_params
from rmndin.users import controllers


usersbp = Blueprint('users', __name__)
verifybp = Blueprint('verify', __name__)


@usersbp.route('/<user_id>/contacts', methods=['POST'])
@require_user_access
@require_params('identifier', 'method')
def create_contact(user_id):
    params = request.get_json()
    return controllers.create_user_contact(params, user_id)


@usersbp.route('/<user_id>/contacts', methods=['GET'])
@require_user_access
def get_contacts(user_id):
    return controllers.get_contacts(user_id)


@verifybp.route('/contact/<hashed_key>')
def verify_contact(hashed_key):
    return controllers.verify_contact(hashed_key)


@verifybp.route('/email/<hashed_key>')
def verify_email(hashed_key):
    return controllers.verify_user(hashed_key)
