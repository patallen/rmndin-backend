from itsdangerous import URLSafeTimedSerializer

from app import app


def serialize_key(payload):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.dumps(payload)


def deserialize_key(key):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.loads(key, max_age=app.config.get('CONTACT_VERIFY_MAX_AGE'))


def create_verify_url(contact_id):
    payload = {"contact_id": contact_id}
    key = serialize_key(payload)
    base_url = app.config['URLS']['BASE_URL']
    return "{}/verify/{}".format(base_url, key)
