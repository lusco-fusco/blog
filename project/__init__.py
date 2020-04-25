from flask import Flask, Response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from project.config.config import ConfigFlask, ConfigDB

# --------------------------------
# Create and config app
# --------------------------------
app = Flask(__name__)

# Config app
app.config.from_object(ConfigFlask)
app.config.from_object(ConfigDB)

# Create database connection
db = SQLAlchemy(app)

# Adds Marshmallow
ma = Marshmallow(app)

# Establish migration path
migrate_dir = ConfigDB.MIGRATION_PATH
migrate = Migrate(app, db, directory=migrate_dir) if migrate_dir != '' else Migrate(app, db)

# --------------------------------
# Register blueprint
# --------------------------------
from project.blueprints.home_blueprint import home_blueprint
from project.blueprints.articles_blueprint import article_blueprint
from project.blueprints.user_blueprint import user_blueprint
from project.blueprints.auth_blueprint import auth_blueprint
from project.blueprints.reaction_blueprint import reaction_blueprint
from project.blueprints.comment_blueprint import comment_blueprint
from project.blueprints.tag_blueprint import tag_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(article_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(reaction_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(tag_blueprint)

# --------------------------------
# Error handlers
# --------------------------------
@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404


@app.errorhandler(400)
def not_found(exc):
    print(exc)
    return Response('<h3>Bad request</h3>'), 400


@app.errorhandler(401)
def not_found(exc):
    return Response('<h3>Unauthorized4</h3>'), 401


@app.errorhandler(403)
def not_found(exc):
    return Response('<h3>Forbidden</h3>'), 403

# --------------------------------
# Populate database
# --------------------------------
#from project.model.role import Role
#Role.populate_database()
