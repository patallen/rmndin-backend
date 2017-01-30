from app import app
from app.contacts import verification

@app.route('/verify/<hashed_key>')
def verify_contact(hashed_key):
	contact = verification.verify_contact(hashed_key)
	if not contact:
		return "Invalid verification link"
	return contact.to_dict()