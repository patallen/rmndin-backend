from flask import Blueprint, request
from rmndin.reminders import controllers

from rmndin.auth.decorators import require_user_access
from rmndin.lib.decorators import require_params

bp = Blueprint('reminders', __name__)


@bp.route('', methods=['POST'])
@require_user_access
@require_params('contacts', 'url', ['countdown', 'eta'])
def add_reminder(user_id):
    params = request.get_json()
    return controllers.add_reminder(params, user_id)
