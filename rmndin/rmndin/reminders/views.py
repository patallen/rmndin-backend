from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from rmndin.reminders import controllers

bp = Blueprint('reminders', __name__)


@bp.route('/', methods=['POST'])
@jwt_required()
def add_reminder():
    params = request.get_json()
    rv = controllers.add_reminder(params)
    return jsonify(rv)
