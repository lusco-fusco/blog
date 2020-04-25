from project import db


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class AbstractModel(object):

    @staticmethod
    def filter(cls, filters):
        return cls.query

    @classmethod
    def find_one(cls, filters=None):
        query = cls.filter(filters) if filters is not None else cls.query
        return query.first()

    @classmethod
    def find_all(cls, filters=None):
        query = cls.filter(filters) if filters is not None else cls.query
        return query.all()

    def insert(self):
        db.session.add(self)
        db.session.flush()

    def create(self):
        self.insert()

    def delete(self):
        db.session.delete(self)
        db.session.flush()
