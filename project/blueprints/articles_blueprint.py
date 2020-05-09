from flask import Blueprint, request, render_template, url_for, session
from werkzeug.utils import redirect

from project import db
from project.blueprints.auth_blueprint import admin_required
from project.model.article import Article
from project.model.reaction import Reaction

article_blueprint = Blueprint('article', __name__)


@article_blueprint.route('/article/all', methods=['GET'])
@admin_required
def list_all():
    return render_template('articles/management.html', articles=Article.find_all())


@article_blueprint.route('/article/<article_id>', methods=['GET'])
def details(article_id):
    article = Article.find_one({'id': article_id})
    # Retrieve and aggregate reactions
    counter_reactions = article.get_reactions()
    # Find user reaction
    reaction = Reaction.find_one({'user_id': session.get('user_id'), 'article_id': article_id})
    user_reaction = reaction.emotion.name if reaction is not None else None
    return render_template('articles/details.html',
                           id=article_id,
                           title=article.title,
                           body=article.body,
                           creation_date=article.creation_date,
                           reactions=counter_reactions,
                           user_reaction=user_reaction,
                           comments=article.comments)


@article_blueprint.route('/article/<article_id>', methods=['DELETE'])
@admin_required
def delete(article_id):
    article = Article.find_one({'id': article_id})
    article.soft_delete()
    db.session.commit()
    return '', 204


@article_blueprint.route('/article/<article_id>/restore', methods=['PATCH'])
@admin_required
def restore(article_id):
    article = Article.find_one({'id': article_id})
    article.restore()
    db.session.commit()
    return '', 200


@article_blueprint.route('/article/<article_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(article_id):
    article = Article.find_one({'id': article_id})
    if request.method == 'GET':
        return render_template('articles/form.html',
                               title=article.title,
                               article_title=article.title,
                               article_body=article.body,
                               is_publish=article.is_publish,
                               header_form='edit article',
                               submit_button='edit')
    elif request.method == 'POST':
        article.title = request.form.get("article_title")
        article.body = request.form.get("article_body")
        article.is_publish = True if request.form.get("article_publish") is not None else False
        article.update()
        db.session.commit()
        return redirect(url_for('article.details', article_id=article.id))


@article_blueprint.route('/article', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'GET':
        return render_template('articles/form.html', title='create article', header_form='create article', submit_button='create')
    elif request.method == 'POST':
        title = request.form.get("article_title")
        body = request.form.get("article_body")
        is_publish = True if request.form.get("article_publish") is not None else False
        article = Article(title=title, body=body, is_publish=is_publish, writer=session.get('user_id'))
        article.create()
        db.session.commit()
        return redirect(url_for('article.details', article_id=article.id))


@article_blueprint.route('/article/search', methods=['GET'])
def search():
    filters = dict()
    q = request.args.get('q')
    writer = request.args.get('writer')
    # TODO: tag = request.args.get('tag')
    if q is not None:
        filters['q'] = q
    if writer is not None:
        filters['writer'] = writer
    filters['is_publish'] = True
    articles = Article.find_all(filters)
    return render_template('articles/search.html', filters=filters, articles=articles)
