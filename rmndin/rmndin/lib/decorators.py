from flask import jsonify, request


def _check_required(req, params):
    if isinstance(req, (list, tuple)) and not any([s in params for s in req]):
            return False
    if req not in params:
        return False
    return True


def require_params(*req):
    def decorator(func):
        def wrapper(*args, **kwargs):
            params = request.get_json().keys()
            valid = all([_check_required(r, params) for r in req])
            if not valid:
                return jsonify({"error":
                                "Missing one or more required params."})
            return func(*args, **kwargs)
        return wrapper
    return decorator
