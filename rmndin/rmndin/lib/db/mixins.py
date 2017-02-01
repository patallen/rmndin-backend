import datetime
import enum

from rmndin import db


class BaseMixin(object):
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    def to_dict(self, exclude=None):
        exclude = exclude or []

        if isinstance(exclude, str):
            exclude = [exclude]

        rv = dict()
        for column in self.__table__.columns:
            name = column.name
            if not name.startswith("_") and name not in exclude:
                value = getattr(self, name)
                if isinstance(value, enum.Enum):
                    value = value.name

                rv[name] = str(value)
        return rv

    @classmethod
    def exists_by_key(cls, key, value, case_sensitive=True):
        column = getattr(cls, key)
        query = db.session.query(cls)
        if case_sensitive:
            query = query.filter(column.ilike(value))
        else:
            query = query.filter(column == value)
        return query.count() > 0

    @classmethod
    def create(cls, add=True, commit=True, *args, **kwargs):
        obj = cls(*args, **kwargs)
        if add:
            db.session.add(obj)
            if commit:
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
        return obj
