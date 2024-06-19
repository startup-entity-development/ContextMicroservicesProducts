import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = os.environ['DB_NAME']
db_password = os.environ['DB_PASSWORD']
db_user = os.environ['DB_USER']
db_uri = os.environ['DB_URI']
pool_recycle = int(os.environ['POOL_RECYCLE'])
pool_size = int(os.environ['POOL_SIZE'])
max_overflow = int(os.environ['MAX_OVERFLOW'])

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_user}:{db_password}@{db_uri}/{db_name}"



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True