from sqlalchemy import Enum as SQLEnum, UniqueConstraint
from project import db
from passlib.apps import custom_app_context as pwd_context

from project.model.abstract.abstract_model_attributes import AbstractModelWithAttributes
from project.model.role import RoleName


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class User(db.Model, AbstractModelWithAttributes):
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(SQLEnum(RoleName), db.ForeignKey("role.name"), default=RoleName.USER)
    __table_args__ = (UniqueConstraint('email', 'remove_date', name='unique_user_email'),)

    def hash_password(self, clear_password):
        self.password_hash = pwd_context.hash(clear_password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_admin(self):
        return self.role == RoleName.ADMIN

    # TODO
    def recommend_articles(self):
        pass

    @classmethod
    def filter(cls, filters):
        query = AbstractModelWithAttributes.filter(cls, filters)

        if 'email' in filters:
            query = query.filter_by(email=filters['email'])
        elif 'role' in filters:
            query = query.filter_by(role=filters['role'])
        elif 'first_name' in filters:
            query = query.filter_by(first_name=filters['first_name'])

        return query
