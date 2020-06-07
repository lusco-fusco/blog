from project import db, ma
from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Tag(db.Model, AbstractModel):
    id = db.Column(db.String(40), primary_key=True)
    articles = db.relationship('ArticleRelationTag', uselist=True, lazy=True)

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter(cls, filters)

        if 'id' in filters:
            query = query.filter_by(id=filters['id'])
        if 'keyword' in filters:
            query = query.filter(Tag.id.ilike('%{}%'.format(filters['keyword'])))
        return query


class ArticleRelationTag(db.Model, AbstractModel):
    tag_id = db.Column(db.String(40), db.ForeignKey("tag.id"), primary_key=True)
    article_id = db.Column(db.String(40), db.ForeignKey("article.id"), primary_key=True)
    article = db.relationship('Article', lazy=True)

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter(cls, filters)

        if 'tag_id' in filters:
            query = query.filter_by(tag_id=filters['tag_id'])
        if 'article_id' in filters:
            query = query.filter_by(article_id=filters['article_id'])
        return query


# -------------------------------------
# Marshmallow schemas
# -------------------------------------
class TagSchema(ma.Schema):
    class Meta:
        fields = ['id']
