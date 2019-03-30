class SimpleDbConfig(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///post.sqlite"


class ProdConfig(SimpleDbConfig):
    pass


class DevConfig(SimpleDbConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(SimpleDbConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_post.sqlite"
