from flask_jwt import current_identity

from rmndin import app, db
from rmndin.lib.db.enums import DeliveryMethodEnum
from rmndin.lib.verification import deserialize_key
from rmndin.users.models import User, UserContact


# @ensure_params(['identifier', 'method'])
def create_user_contact(params, user_id):
    allowed = user_has_access(current_identity, user_id)
    if not allowed:
        return {"error": "Access denied."}

    identifier = params.get('identifier')
    method = params.get('method')
    enumed_method = DeliveryMethodEnum(method)
    query = db.session.query(UserContact)

    f_method = (UserContact.method == enumed_method)
    f_id = (UserContact.identifier == identifier)
    f_verified = (UserContact.verified.is_(True))

    existing = query.filter(f_method, f_verified, f_id).all()
    if len(existing):
        return {"errors":
                "This identifier already exists in our database."}

    f_unverified = (UserContact.verified.is_(False))
    f_user = (UserContact.user_id == user_id)

    exists_for_user = query.filter(f_unverified, f_user, f_id).all()

    if exists_for_user:
        return {"errors":
                "You've got a pending verification for this contact."}

    contact = UserContact.create(user_id=user_id,
                                 identifier=identifier,
                                 method=enumed_method)

    vehicle = contact.get_vehicle()
    vehicle.send_verification()

    return {"success":
            "Contact created. You must verify it before it can be used."}


def verify_contact(hashed_key):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    max_age = app.config['CONTACT_VERIFY_MAX_AGE']
    print hashed_key, secret_key, max_age
    try:
        info = deserialize_key(hashed_key, secret_key, max_age)
    except Exception as e:
        print(e)
        return {"error": "Invalid verification link."}

    contact_id = info['contact_id']
    contact = db.session.query(UserContact).get(contact_id)
    if contact:
        contact.verified = True
        db.session.add(contact)
        db.session.commit()
        return {"success": contact.to_dict()}
    else:
        return {"error": "Contact no longer exists"}


def verify_user(hashed_key):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    max_age = app.config['CONTACT_VERIFY_MAX_AGE']
    try:
        info = deserialize_key(hashed_key, secret_key, max_age)
    except Exception as e:
        print(e)
        return {"error": "Invalid verification link."}

    email = info.get('email')
    user = User.query.filter_by(email=email).first()

    if user and user.verified:
        return {"error": "You are already verified. Log in."}
    elif user and not user.verified:
        user.verified = True
        contact = UserContact(method='email', identifier=email,
                              verified=True, user_id=user.id)
        db.session.add(user)
        db.session.add(contact)
        db.session.commit()
        return {"success": "You are now verified! Please log in."}
    else:
        return {"error": "Invalid verification link."}


def user_has_access(user, user_id=None):
    if int(user.id) == int(user_id):
        return True
    return False


def get_contacts(params, user_id):
    allowed = user_has_access(current_identity, user_id)
    if not allowed:
        return {"error": "Access denied."}

    contacts = UserContact.query.filter_by(user_id=user_id).all()
    return {"success": [c.to_dict() for c in contacts]}
