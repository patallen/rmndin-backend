from flask import Blueprint

from rmndin.auth import controllers
from rmndin.lib.web.request import get_params

bp = Blueprint('auth', __name__)


@bp.route('/auth/signup', methods=["POST"])
def user_registration():
    params = get_params()
    return controllers.user_registration(params)
