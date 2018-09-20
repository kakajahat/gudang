class Config(object):
    """
    config umumnya disini.
    """
    pass


class DevelopmentConfig(Config):
    """
    dev config disini
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Config kalo udah di production state
    """
    Debug = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
