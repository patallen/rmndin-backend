from flask import Blueprint, jsonify, request

from rmndin.auth import controllers


auth = Blueprint('auth', __name__)


@auth.route('/auth/signup', methods=["POST"])
def user_registration():
    params = request.get_json()
    rv = controllers.user_registration(params)
    return jsonify(rv)