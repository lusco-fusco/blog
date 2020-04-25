from flask import Blueprint, request, session

from project import db
from project.blueprints.auth_blueprint import login_required
from project.model.article import Article
from project.model.reaction import Reaction, Emotions

reaction_blueprint = Blueprint('reaction', __name__)


@reaction_blueprint.route('/reaction/<article_id>', methods=['POST'])
@login_required
def react_an_article(article_id):
    if Article.find_one({'id': article_id, 'is_publish': True, 'enabled': True}) is not None:
        reaction = Reaction.find_one({'user_id': session.get('user_id'), 'article_id': article_id})
        if reaction is None:
            emotion = Emotions(request.json.get('emotion').upper())
            reaction = Reaction(user_id=session.get('user_id'), article_id=article_id, emotion=emotion)
            reaction.create()
        else:
            reaction.emotion = Emotions(request.json.get('emotion').upper())
        db.session.commit()
    return 'ok'

