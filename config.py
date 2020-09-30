class Config(object):
    DEBUG = False
    TESTING = False

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "password"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING =  True