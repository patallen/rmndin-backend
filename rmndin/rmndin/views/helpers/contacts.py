from rmndin import db
from rmndin.models import UserContact, DeliveryMethodEnum

from rmndin.contacts.verification import deserialize_key


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

    vehicle = contact.get_vehicle()
    vehicle.send_verification()

    return True, "Contact created. Please verify."


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