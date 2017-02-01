from flask import jsonify

from app import app
from app.views import helpers


@app.route('/verify/contact/<hashed_key>')
def verify_contact(hashed_key):
    contact = helpers.contacts.verify_contact(hashed_key)
    if not contact:
        return "Invalid verification link."
    return jsonify(contact.to_dict())


@app.route('/verify/email/<hashed_key>')
def verify_email(hashed_key):
    user, code = helpers.users.verify_user(hashed_key)
    if not user:
        msg = "Could not verify due to %s." % code
    else:
        msg = "Success! Please log in :)"
    return jsonify(msg)
