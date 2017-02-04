import datetime
import enum
import warnings

import rmndin
from rmndin import db


class BaseMixin(object):
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize. Set the db and session."""
        super(BaseMixin, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Repr based on the '__repr_columns__' class variable of the model."""
        cls_name = self.__class__.__name__

        if not hasattr(self, '__repr_columns__'):
            warning = (
                "%s model is missing the __repr_columns__ class variable. "
                "This should be utilized for ease of debugging." % cls_name
            )
            warnings.warn(warning)
            return super(BaseMixin, self).__repr__()

        rs = ""
        for col in self.__repr_columns__:
            val = getattr(self, col)
            if isinstance(val, basestring):
                val = '"%s"' % val
            elif isinstance(val, enum.Enum):
                val = val.value
            rs = "%s%s" % (rs, ' %s=%s' % (col, val))

        return "<%s:%s>" % (cls_name, rs)

    def to_dict(self, exclude=None):
        """Return a dictionary of the model instance."""
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
        """Check if more than 1 instance exists in the database by key."""
        column = getattr(cls, key)
        query = db.session.query(cls)
        if case_sensitive:
            query = query.filter(column.ilike(value))
        else:
            query = query.filter(column == value)
        return query.count() > 0

    @classmethod
    def create(cls, add=True, commit=True, *args, **kwargs):
        """Create the model instance. Add and commit as requested."""
        obj = cls(*args, **kwargs)
        if add:
            db.session.add(obj)
            if commit:
                rmndin.lib.db.commit_session(db)
        return obj

    @property
    def db(self):
        return db

    @property
    def session(self):
        return db.session

    def commit_session(self):
        """Commit the session."""
        rmndin.lib.db.commit_session(self.db)

    def save(self):
        """Add instance to the session and commit."""
        self.session.add(self)
        self.commit_session()
