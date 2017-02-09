from rmndin import app, db, success, error
from rmndin.lib.db.enums import DeliveryMethodEnum
from rmndin.lib.verification import deserialize_key
from rmndin.users.models import User, UserContact
from rmndin.lib.web.request import get_params

def create_user_contact(params, user_id):
    identifier = params.get('identifier')
    method = params.get('method')
    enumed_method = DeliveryMethodEnum(method)
    query = db.session.query(UserContact)

    f_method = (UserContact.method == enumed_method)
    f_id = (UserContact.identifier == identifier)
    f_verified = (UserContact.verified.is_(True))

    existing = query.filter(f_method, f_verified, f_id).all()
    if len(existing):
        return error(message="This identifier already exists in our database.")

    f_unverified = (UserContact.verified.is_(False))
    f_user = (UserContact.user_id == user_id)

    exists_for_user = query.filter(f_unverified, f_user, f_id).all()

    if exists_for_user:
        return error(
            message="You've got a pending verification for this contact.")

    contact = UserContact(user_id=user_id, identifier=identifier,
                          method=enumed_method)

    vehicle = contact.get_vehicle()
    saved, err = vehicle.send_and_save_contact()

    if not saved:
        return error(
            message="We had a problem creating this contact.",
            errors=[err],
            status="bad_request"
        )

    return success(
        contact.to_dict(),
        message="Contact created. You must verify it before it can be used.",
        status='created'
    )

def delete_contact(contact_id):
    del_cout = UserContact.query.delete(contact_id)
    if del_count < 1:
        return error(message="No contact found.", status="not_found")

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return error(message="Something went wrong.", status="bad_request")
    return success("Successfully deleted!", status="success")

def verify_contact(hashed_key):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    max_age = app.config['CONTACT_VERIFY_MAX_AGE']

    try:
        info = deserialize_key(hashed_key, secret_key, max_age)
    except Exception as e:
        print(e)
        return error("Invalid verification link.")

    contact_id = info['contact_id']
    contact = db.session.query(UserContact).get(contact_id)
    if contact:
        contact.verified = True
        db.session.add(contact)
        db.session.commit()
        return success('You may now use your new contact!')
    else:
        return error('Contact no longer exists', status='not_found')


def verify_user(hashed_key):
    secret_key = app.config['CONTACT_VERIFY_SECRET']
    max_age = app.config['CONTACT_VERIFY_MAX_AGE']
    try:
        info = deserialize_key(hashed_key, secret_key, max_age)
    except Exception as e:
        print(e)
        return error("Invalid verification link.")

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
        return success("You are now verified! Please log in.")
    else:
        return error("Invalid verification link.")


def get_contacts(user_id):
    contacts = UserContact.query.filter_by(user_id=user_id).all()
    return success(data=[c.to_dict() for c in contacts])
