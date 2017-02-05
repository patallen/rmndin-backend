from rmndin import db
from rmndin.lib.db.mixins import BaseMixin


reminder_contact = db.Table(
    'reminder_contact_association',
    db.Column('reminder_id', db.Integer,
              db.ForeignKey('reminder.id', onupdate="CASCADE",
                            ondelete="CASCADE")),
    db.Column('user_contact_id', db.Integer,
              db.ForeignKey('user_contact.id', onupdate="CASCADE",
                            ondelete="CASCADE"))
)


class Reminder(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"),
    )
    task_id = db.Column(db.String(36))
    url = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=True)
    eta = db.Column(db.DateTime, nullable=False)
    fulfilled = db.Column(db.Boolean, nullable=False, default=False)

    contacts = db.relationship("UserContact", secondary=reminder_contact,
                               backref="reminders", cascade="all")

    __repr_columns__ = ['user_id', 'url', 'eta']
    __default_excludes__ = ['task_id']

    def add_contact(self, contact, commit=True):
        self.add_contacts([contact], commit=commit)

    def add_contacts(self, contacts, commit=True):
        for contact in contacts:
            self.contacts.append(contact)
        if commit:
            self.commit_session()

    def to_dict(self, include_contacts=False, *args, **kwargs):
        rv = super(Reminder, self).to_dict(*args, **kwargs)
        if include_contacts:
            excl = ['created', 'updated']
            rv["contacts"] = [c.to_dict(exclude=excl) for c in self.contacts]
        return rv
