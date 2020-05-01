from collections import Counter

from project import db
from project.model.abstract.abstract_model_attributes import AbstractModelWithAttributes


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Article(db.Model, AbstractModelWithAttributes):
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    is_publish = db.Column(db.Boolean(), default=False, nullable=False)
    writer = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    reactions = db.relationship('Reaction', uselist=True, lazy=True)
    comments = db.relationship('Comment', uselist=True, lazy=True, primaryjoin="and_(Article.id==Comment.article_id, Comment.enabled==True)")
    tags = db.relationship('ArticleRelationTag', uselist=True, lazy=True)

    @classmethod
    def filter(cls, filters):
        query = AbstractModelWithAttributes.filter(cls, filters)

        if 'is_publish' in filters:
            query = query.filter_by(is_publish=filters['is_publish'])
        if 'title' in filters:
            query = query.filter(Article.title.ilike('%{}%'.format(filters['title'])))
        if 'body' in filters:
            query = query.filter(Article.body.ilike('%{}%'.format(filters['body'])))
        if 'writer' in filters:
            query = query.filter_by(writer=filters['writer'])
        return query

    # TODO
    def get_tags_as_string(self):
        pass

    # TODO
    def save_tag_from_string(self, tags_as_string):
        pass

    def get_reactions(self):
        counter_reactions = Counter()
        for emotion in list(map(lambda x: x.emotion.name, self.reactions)):
            counter_reactions[emotion] += 1
        return counter_reactions

    def check_unique_reactions(self, x):
        return x in set(list(map(lambda x: x.emotion.name, self.reactions)))

    def get_number_of_reactions(self):
        return len(self.reactions)

    # TODO
    def get_similar_articles(self):
        pass
