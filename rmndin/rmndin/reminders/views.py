from flask import Blueprint
from rmndin.reminders import controllers

from rmndin.auth.decorators import require_user_access
from rmndin.lib.decorators import require_params
from rmndin.lib.web.request import get_params


bp = Blueprint('reminders', __name__)


@bp.route('', methods=['POST'])
@require_user_access
@require_params('contacts', 'url', ['countdown', 'eta'])
def add_reminder(user_id):
    params = get_params()
    return controllers.add_reminder(params, user_id)
