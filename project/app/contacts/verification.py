from itsdangerous import URLSafeTimedSerializer

from app import app, db
from app.models import UserContact, DeliveryMethodEnum


def create_contact(user_id, method, identifier):
    enumed_method = DeliveryMethodEnum(method)
    query = db.session.query(UserContact)

    f_method = (UserContact.method == enumed_method)
    f_id = (UserContact.identifier == identifier)
    f_verified = (UserContact.verified.is_(True))

    existing = query.filter(f_method, f_verified, f_id).all()
    if len(existing):
        return False, "This identifier already exists in our database"

    f_unverified = (UserContact.verified.is_(False))
    f_user = (UserContact.user_id == user_id)

    exists_for_user = query.filter(f_unverified, f_user).all()

    if exists_for_user:
        print "Existing: %s" % exists_for_user

        return False, "You've tried this already. Please verify."

    contact = UserContact(user_id=user_id,
                          identifier=identifier,
                          method=enumed_method)
    db.session.add(contact)
    db.session.commit()

    send_contact_verification(contact)

    return True, "Contact created. Please verify."


def send_contact_verification(contact):
    vehicle = contact.get_vehicle()
    vehicle.send_verification()



def serialize_key(payload):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.dumps(payload)

def deserialize_key(key):
    s = URLSafeTimedSerializer(app.config.get('CONTACT_VERIFY_SECRET'))
    return s.loads(key, max_age=app.config.get('CONTACT_VERIFY_MAX_AGE'))


def verify_contact(hashed_key):
    try:
        info = deserialize_key(hashed_key)
    except Exception as e:
        print(e)
        return False

    contact_id = info['contact_id']
    contact = db.session.query(UserContact).get(contact_id)
    if contact:
        contact.verified = True
        db.session.add(contact)
        db.session.commit()
        return contact
    else:
        return None

def create_verify_url(contact_id):
    payload = {"contact_id": contact_id}
    key = serialize_key(payload)
    base_url = app.config['URLS']['BASE_URL']
    return "{}/verify/{}".format(base_url, key)
