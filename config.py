class Config(object):
    DEBUG = False
    TESTING = False

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "password"
    ENVDATA_API_URL_HISTORICAL = "https://i3.zapto.org/bdm01/getEnvDataByTime.php"
    ENVDATA_API_URL_LIVE = "https://i3.zapto.org/bdm01/getEnvDataByDuration.php"
    FANUC_API_URL_HISTORICAL ="https://i3.zapto.org/bdm01/getFanucDataByTime.php"
    FANUC_API_URL_LIVE = "https://i3.zapto.org/bdm01/getFanucDataByDuration.php"
    MOLDMASTER_API_URL_HISTORICAL = "https://i3.zapto.org/bdm01/getMoldMasterDataByTime.php"
    MOLDMASTER_API_URL_LIVE ="https://i3.zapto.org/bdm01/getMoldMasterDataByDuration.php"
    MOULDFLO_API_URL_HISTORICAL = "https://i3.zapto.org/bdm01/getMouldfloDataByTime.php"
    MOULDFLO_API_URL_LIVE = "https://i3.zapto.org/bdm01/getMouldfloDataByDuration.php"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING =  True