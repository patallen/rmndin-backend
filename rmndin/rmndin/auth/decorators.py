from flask import jsonify

from flask_jwt import jwt_required, current_identity
import functools


def require_user_access(func):

    @jwt_required()
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if not current_identity.has_access(kwargs.get('user_id')):
            return jsonify({"error": "Access denied."})
        return func(*args, **kwargs)

    return decorated

