class Config(object):
    DEBUG = False
    TESTING = False

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "password"
    ENVDATA_API_URL_HISTORICAL = "https://i3.zapto.org/bdm01/getEnvDataByTime.php"
    ENVDATA_API_URL_LIVE = "https://i3.zapto.org/bdm01/getEnvDataByDuration.php"
    FANUC_API_URL_HISTORICAL ="https://i3.zapto.org/bdm01/getEnvDataByTime.php"
    FANUC_API_URL_LIVE = "https://i3.zapto.org/bdm01/getFanucDataByDuration.php"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING =  True