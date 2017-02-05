from werkzeug.wrappers import Response
import json


STATUS_MAP = {
    "success": (200, "The request was successful."),
    "created": (201, "Entity was successfully created."),
    "bad_request": (400, "Could not fulfill request."),
    "not_found": (404, "Resource could not be found."),
    "unauthorized": (401, "Please log in."),
    "forbidden": (403, "Access denied."),
    "access_denied": (403, "Access denied."),
}


class RmndinResponse(Response):
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, XHRResponse):
            rv = cls._make_response(rv)
        return super(RmndinResponse, cls).force_type(rv, environ)

    @classmethod
    def _make_response(cls, xhrobject):
        return xhrobject.make_response(cls)


def _get_status_info(name):
    code, desc = STATUS_MAP.get(name, (False, None))
    if not code:
        raise Exception("Status Code %s is invalid." % name)
    return code, desc


class XHRResponse(Response):
    mimetype = 'application/json'
    ok_statuses = (200, 201)

    def __init__(self, message=None, data=None, errors=None,
                 status='success', headers=None, meta=None):
        self._errors = None
        self._headers = None
        self._status_key = None
        self._status_code = None
        self._status_description = None

        self.message = message

        self._meta = meta

        self.status = status
        self.errors = errors
        self.headers = headers or {}

        self._data = data

    @property
    def json_data(self):
        """Return the json dumped data."""
        rv = {}
        rv['status_code'] = self.status_code
        if self.status_is_ok:
            rv['description'] = self.message or self._status_description
            if self.data:
                rv['data'] = self.data
        else:
            rv['description'] = self.message
            if self.errors:
                rv['errors'] = self.errors
        return json.dumps(rv, default=lambda o: o.isoformat())

    @property
    def data(self):
        return self._data

    @property
    def status(self):
        """Return the underlying status key."""
        return self._status

    @status.setter
    def status(self, status):
        code, desc = _get_status_info(status)
        self._status = status
        self._status_code = code
        self._status_description = desc

    @property
    def status_code(self):
        """Return the underlying status_code."""
        return self._status_code

    @property
    def status_is_ok(self):
        """Return whether or not the status is acceptable."""
        return (self.status_code in self.ok_statuses)

    def make_response(self, response_class):
        res = response_class()
        res.data = self.json_data
        res.status_code = self.status_code
        res.headers.extend(self.headers)
        return res


class XHRError(XHRResponse):
    def __init__(self, message, status="bad_request", **kwargs):
        return super(XHRError, self).__init__(message=message,
                                              status=status, **kwargs)


class XHRSuccess(XHRResponse):
    def __init__(self, data, status="success", **kwargs):
        return super(XHRSuccess, self).__init__(data=data, status=status, **kwargs)
