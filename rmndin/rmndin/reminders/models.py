from rmndin import db
from rmndin.lib.db.mixins import BaseMixin


reminder_contact = db.Table(
    'reminder_contact_association',
    db.Column('reminder_id', db.Integer, db.ForeignKey('reminder.id')),
    db.Column('user_contact_id', db.Integer, db.ForeignKey('user_contact.id'))
)


class Reminder(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(36), nullable=True)
    body = db.Column(db.String)
    eta = db.Column(db.DateTime, nullable=False)
    fulfilled = db.Column(db.Boolean, nullable=False, default=False)

    contacts = db.relationship("UserContact", secondary=reminder_contact,
                               backref="reminders")

    __repr_columns__ = ['user_id', 'body', 'eta']

    def add_contact(self, contact, commit=True):
        self.add_contacts([contact], commit=commit)

    def add_contacts(self, contacts, commit=True):
        for contact in contacts:
            self.contacts.append(contact)
        if commit:
            self.commit_session()
