from flask import Blueprint, request, session, url_for
from werkzeug.utils import redirect

from project import db
from project.blueprints.auth_blueprint import login_required
from project.model.article import Article
from project.model.comment import Comment

comment_blueprint = Blueprint('comment', __name__)


@comment_blueprint.route('/comment/<article_id>', methods=['POST'])
@login_required
def create(article_id):
    if Article.find_one({'id': article_id, 'is_publish': True, 'enabled': True}) is not None:
        Comment(article_id=article_id, user_id=session.get('user_id'), text=request.form.get('comment_text')).create()
        db.session.commit()
    return redirect(url_for('article.details', article_id=article_id))


@comment_blueprint.route('/comment/<comment_id>', methods=['DELETE'])
@login_required
def delete(comment_id):
    comment = Comment.find_one({'id': comment_id})
    if comment.user_id == session.get('user_id') or session.get('is_admin'):
        comment.soft_delete()
        db.session.commit()
        return '', 204
    else:
        return 401
