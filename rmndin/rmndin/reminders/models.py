from rmndin import db
from rmndin.lib.db.mixins import BaseMixin
from rmndin.lib.db.enums import DeliveryMethodEnum


class Reminder(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(36), nullable=True)
    body = db.Column(db.String)
    eta = db.Column(db.DateTime, nullable=False)
    type_ = db.Column(db.String, nullable=False)
    delivery_method = db.Column(db.Enum(DeliveryMethodEnum), nullable=False)

    fulfilled = db.Column(db.String, nullable=False, default=False)
