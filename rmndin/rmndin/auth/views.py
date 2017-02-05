from flask import Blueprint, request

from rmndin.auth import controllers


bp = Blueprint('auth', __name__)


@bp.route('/auth/signup', methods=["POST"])
def user_registration():
    params = request.get_json()
    return controllers.user_registration(params)
