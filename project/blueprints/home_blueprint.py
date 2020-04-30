from flask import Blueprint, render_template

from project.model.article import Article

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/', methods=['GET'])
def list_publish_articles():
    articles = Article.find_all({'is_publish': True, 'enabled': True})
    return render_template('home.html', title='home', articles=articles)
