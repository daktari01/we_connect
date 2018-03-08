# config.py
class Config(object):
    """Default configuration"""

    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Development configuration"""
    DEBUG = False
    TESTING = False

app_config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "testing" : TestingConfig
}