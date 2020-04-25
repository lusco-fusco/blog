from enum import Enum
from sqlalchemy import Enum as SQLEnum

from project import db
from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# Enum
# -------------------------------------
class RoleName(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Role(db.Model, AbstractModel):
    name = db.Column(SQLEnum(RoleName), primary_key=True)

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter(cls, filters)

        if 'name' in filters:
            query = query.filter_by(id=filters['name'])

        return query

    @staticmethod
    def populate_database():
        if len(Role.find_all() < 2):
            Role(RoleName.ADMIN).create()
            Role(RoleName.USER).create()
            db.session.commit()
