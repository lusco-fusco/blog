from flask import Blueprint, request, render_template, url_for, session
from werkzeug.utils import redirect

from project import db
from project.blueprints.auth_blueprint import admin_required
from project.model.article import Article
from project.model.reaction import Reaction

article_blueprint = Blueprint('article', __name__)


@article_blueprint.route('/articles', methods=['GET'])
def all_articles():
    articles = Article.find_all({'enabled': True})
    return render_template('articles/list.html', articles=articles)


@article_blueprint.route('/article/<article_id>', methods=['GET', 'DELETE'])
def single_article(article_id):
    if request.method == 'GET':
        article = Article.find_one({'id': article_id})
        # Retrieve and aggregate reactions
        counter_reactions = article.get_reactions()
        # Find user reaction
        reaction = Reaction.find_one({'user_id': session.get('user_id'), 'article_id': article_id})
        user_reaction = reaction.emotion.name if reaction is not None else None
        return render_template('articles/info.html',
                               id=article_id,
                               title=article.title,
                               body=article.body,
                               creation_date=article.creation_date,
                               reactions=counter_reactions,
                               user_reaction=user_reaction,
                               comments=article.comments)
    elif request.method == 'DELETE':
        article = Article.find_one({'id': article_id})
        article.soft_delete()
        db.session.commit()
        return '', 204


@article_blueprint.route('/article/<article_id>/edit', methods=['GET', 'POST'])
@admin_required
def render_edit_article(article_id):
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
        return redirect(url_for('article.single_article', article_id=article.id))


@article_blueprint.route('/article', methods=['GET', 'POST'])
@admin_required
def create_article():
    if request.method == 'GET':
        return render_template('articles/form.html', title='create article', header_form='create article', submit_button='create')
    elif request.method == 'POST':
        title = request.form.get("article_title")
        body = request.form.get("article_body")
        is_publish = True if request.form.get("article_publish") is not None else False
        article = Article(title=title, body=body, is_publish=is_publish, writer=session.get('user_id'))
        article.create()
        db.session.commit()
        return redirect(url_for('article.single_article', article_id=article.id))
