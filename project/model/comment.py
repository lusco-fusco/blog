from sqlalchemy import func, DateTime

from project import db
from project.model.abstract.abstract_model_attributes import AbstractModelWithAttributes


class Comment(db.Model, AbstractModelWithAttributes):
    user_id = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.String(40), db.ForeignKey('article.id'), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    creation_date = db.Column(DateTime(timezone=True), default=func.now(), nullable=False)
    commenter = db.relationship('User', lazy=True)

    @classmethod
    def filter(cls, filters):
        query = AbstractModelWithAttributes.filter(cls, filters)

        if 'user_id' in filters:
            query = query.filter_by(user_id=filters['user_id'])
        if 'article_id' in filters:
            query = query.filter_by(article_id=filters['article_id'])
        if 'text' in filters:
            query = query.filter(Comment.text.ilike('%{}%'.format(filters['text'])))
        return query
