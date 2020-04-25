from enum import Enum
from sqlalchemy import Enum as SQLEnum, func, DateTime

from project import db
from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# Enum
# -------------------------------------
class Emotions(Enum):
    IDEA = 'IDEA'
    BUG = 'BUG'
    CLAP = 'CLAP'
    LOVE = 'LOVE'
    PARTY = 'PARTY'
    WIZARD = 'WIZARD'


class Reaction(db.Model, AbstractModel):
    user_id = db.Column(db.String(40), db.ForeignKey('user.id'), primary_key=True)
    article_id = db.Column(db.String(40), db.ForeignKey('article.id'), primary_key=True)
    emotion = db.Column(SQLEnum(Emotions), nullable=False)
    creation_date = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter(cls, filters)

        if 'user_id' in filters:
            query = query.filter_by(user_id=filters['user_id'])
        if 'article_id' in filters:
            query = query.filter_by(article_id=filters['article_id'])

        return query