from project.config.environment import get_env

# Load the environment
env = get_env()


class ConfigFlask(object):
    DEBUG = env.get('DEBUG')
    CSRF_ENABLED = env.get('CSRF_ENABLED')
    HOST = env.get('HOST')
    PORT = env.get('PORT')
    SECRET_KEY = env.get('SECRET_KEY')


class ConfigDB(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        env.get('DATABASE_USER'),
        env.get('DATABASE_PASSWORD'),
        env.get('DATABASE_HOST'),
        env.get('DATABASE_PORT'),
        env.get('DATABASE_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = env.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    MIGRATION_PATH = env.get('MIGRATION_PATH')
    SQLALCHEMY_ECHO = env.get('SQLALCHEMY_ECHO')
