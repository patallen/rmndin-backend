from itsdangerous import URLSafeTimedSerializer


def serialize_key(payload, secret_key):
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps(payload)


def deserialize_key(key, secret_key, max_age):
    s = URLSafeTimedSerializer(secret_key)
    return s.loads(key, max_age=max_age)


def make_verify_url(payload, verify_type, base_url, secret_key):
    key = serialize_key(payload, secret_key)
    return "{}/verify/{}/{}".format(base_url, verify_type, key)


def contact_verify_url(contact_id, base_url, secret_key):
    payload = {"contact_id": contact_id}
    return make_verify_url(payload, 'contact', base_url, secret_key)


def email_verify_url(email, base_url, secret_key):
    payload = {
        "email": email,
        "primary": True
    }
    return make_verify_url(payload, 'email', base_url, secret_key)
