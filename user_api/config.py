import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///userdb.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    KEY_LIST_PATH = os.path.join(os.path.dirname(__file__), "keys/keylist.json")
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    KEY_LIST_PATH = os.path.join(os.path.dirname(__file__), "tests/keys/keylist.json")
    SQLALCHEMY_DATABASE_URI = r"sqlite:///tests/test_userdb.sqlite"