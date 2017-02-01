from itsdangerous import URLSafeTimedSerializer

from rmndin import app


def serialize_key(payload):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.dumps(payload)


def deserialize_key(key):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.loads(key, max_age=app.config.get('CONTACT_VERIFY_MAX_AGE'))


def make_verify_url(payload, verify_type):
    base_url = app.config['URLS']['BASE_URL']
    key = serialize_key(payload)
    return "{}/verify/{}/{}".format(base_url, verify_type, key)


def contact_verify_url(contact_id):
    payload = {"contact_id": contact_id}
    return make_verify_url(payload, 'contact')


def email_verify_url(email):
    payload = {
        "email": email,
        "primary": True
    }
    return make_verify_url(payload, 'email')
