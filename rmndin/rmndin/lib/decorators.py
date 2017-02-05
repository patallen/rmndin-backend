from rmndin import error
from rmndin.lib.web.request import get_params


def _check_required(req, params):
    if isinstance(req, (list, tuple)):
        return any([r in params for r in req])
    if req not in params:
        return False
    return True


def require_params(*req):
    def decorator(func):
        def wrapper(*args, **kwargs):
            given = map(str, list(get_params()))
            if not all([_check_required(r, given) for r in req]):
                return error(
                    message="Missing one or more required params.",
                    status="bad_request"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
