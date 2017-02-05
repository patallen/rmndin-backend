from flask import request
from rmndin import error


def _check_required(req, params):
    if isinstance(req, (list, tuple)):
        return any([r in params for r in req])
    if req not in params:
        return False
    return True


def require_params(*req):
    def decorator(func):
        def wrapper(*args, **kwargs):
            params = request.get_json().keys()
            given = [str(p) for p in params]
            if not all([_check_required(r, given) for r in req]):
                return error(
                    message="Missing one or more required params.",
                    status="bad_request"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
