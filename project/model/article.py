from collections import Counter

from project import db
from project.model.abstract.abstract_model_attributes import AbstractModelWithAttributes


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
from project.model.tag import Tag, ArticleRelationTag


class Article(db.Model, AbstractModelWithAttributes):
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(240), nullable=True)
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
        if 'subtitle' in filters:
            query = query.filter(Article.subtitle.ilike('%{}%'.format(filters['subtitle'])))
        if 'body' in filters:
            query = query.filter(Article.body.ilike('%{}%'.format(filters['body'])))
        if 'q' in filters:
            query = query.filter(Article.body.ilike('%{}%'.format(filters['q']))
                                 | Article.title.ilike('%{}%'.format(filters['q'])))
        if 'writer' in filters:
            query = query.filter_by(writer=filters['writer'])
        return query

    def attach_tags(self, tag_as_string):
        # Analyze establish and incoming tags
        established_tags = set([r.tag_id for r in self.tags])
        incoming_tags = set(tag_as_string.split(','))

        add_tag = incoming_tags - established_tags
        remove_tag = established_tags - incoming_tags

        # Attach new tags
        for keyword in list(add_tag):
            tag = Tag.find_one({'id': keyword})

            if tag is None:
                tag = Tag(id=keyword)
                tag.create()

            relation = ArticleRelationTag(tag_id=tag.id, article_id=self.id)
            relation.create()
            self.tags.append(relation)

        # Remove old tags
        for tag_id in list(remove_tag):
            ArticleRelationTag.find_one({'tag_id': tag_id}).delete()

    def get_attached_tags(self):
        return ','.join(r.tag_id for r in self.tags)

    def get_tags(self):
        return [r.tag_id for r in self.tags]

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
