from flask import jsonify

from app import app
from app.views.helpers import contacts


@app.route('/verify/<hashed_key>')
def verify_contact(hashed_key):
	contact = contacts.verify_contact(hashed_key)
	if not contact:
		return "Invalid verification link"
	return jsonify(contact.to_dict())