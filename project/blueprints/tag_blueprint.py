from flask import Blueprint, url_for, jsonify, render_template
from werkzeug.utils import redirect

from project.blueprints.auth_blueprint import login_required
from project.model.tag import Tag, TagSchema

tag_blueprint = Blueprint('tag', __name__)
tag_schema = TagSchema(many=True)


@tag_blueprint.route('/tag/<keyword>', methods=['GET'])
@login_required
def find_by_keyword(keyword):
    tags = Tag.find_all({'keyword': keyword})
    return jsonify(tag_schema.dump(tags)), 200


@tag_blueprint.route('/tag/<tag_id>/articles', methods=['GET'])
def related_articles(tag_id):
    tag = Tag.find_one({'id': tag_id})
    if tag is not None:
        # TODO: Improve next "query"
        articles = list(filter(lambda x: x.is_publish and x.enabled, map(lambda x: x.article, tag.articles)))
        return render_template('articles/search.html', filters={'tag': tag_id}, articles=articles)
    return 404
