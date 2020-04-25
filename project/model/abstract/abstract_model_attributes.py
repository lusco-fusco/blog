import uuid
from project import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from project.model.abstract.abstract_model import AbstractModel


def _generate_uuid():
    """
        Generates a universally unique identifier for an database entity

        :return: the universally unique identifier
    """
    return uuid.uuid4().hex


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class AbstractModelWithAttributes(AbstractModel, object):
    id = db.Column(db.String(40), default=_generate_uuid, primary_key=True)
    creation_date = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modification_date = db.Column(DateTime(timezone=True), nullable=True)
    remove_date = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)    # TODO: change default
    enabled = db.Column(db.Boolean(), default=True, nullable=False)

    @staticmethod
    def filter(cls, filters):
        query = super().filter(cls, filters)

        if 'id' in filters:
            query = query.filter_by(id=filters['id'])
        if 'enabled' in filters:
            query = query.filter_by(enabled=filters['enabled'])

        return query

    def update(self):
        self.modification_date = func.now()
        self.insert()

    def soft_delete(self):
        self.enabled = False
        self.remove_date = func.now()
        self.insert()
