import os

from environs import Env
from os import path


def get_env():
    if path.exists(os.getcwd() + '/.env'):
        # Load env file
        env = Env()
        env.read_env(os.getcwd() + '/.env')
        # Retrieve the values:
        # Flask application
        env.bool("DEBUG")
        env.bool("CSRF_ENABLED")
        env.str("HOST")
        env.int("PORT")
        env.str("SECRET_KEY")
        # Postgres database
        env.str("DATABASE_USER")
        env.str("DATABASE_PASSWORD")
        env.str("DATABASE_HOST")
        env.str("DATABASE_PORT")
        env.str("DATABASE_NAME")
        # SqlAlchemy
        env.str("SQLALCHEMY_TRACK_MODIFICATIONS")
        env.str("MIGRATION_PATH")
        env.bool("SQLALCHEMY_ECHO")
        return env.dump()
    env = dict()
    # Retrieve the values:
    # Flask application
    env['DEBUG'] = bool(os.getenv('DEBUG')) or None
    env['CSRF_ENABLED'] = bool(os.getenv('CSRF_ENABLED')) or None
    env['HOST'] = os.getenv('HOST') or None
    env['PORT'] = int(os.getenv('PORT') or 5000)
    env['SECRET_KEY'] = os.getenv('SECRET_KEY') or None
    # Postgres database
    env['DATABASE_USER'] = os.getenv('DATABASE_USER') or None
    env['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD') or None
    env['DATABASE_HOST'] = os.getenv('DATABASE_HOST') or None
    env['DATABASE_PORT'] = os.getenv('DATABASE_PORT') or None
    env['DATABASE_NAME'] = os.getenv('DATABASE_NAME') or None
    # SqlAlchemy
    env['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") or True
    env['MIGRATION_PATH'] = os.getenv('MIGRATION_PATH') or ''
    env['SQLALCHEMY_ECHO'] = bool(os.getenv('SQLALCHEMY_ECHO')) or None
    return env
