from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from rmndin.reminders import controllers

from rmndin.auth.decorators import require_user_access


bp = Blueprint('reminders', __name__)


@bp.route('', methods=['POST'])
@require_user_access
def add_reminder(user_id):
    params = request.get_json()
    rv = controllers.add_reminder(params, user_id)
    return jsonify(rv)
