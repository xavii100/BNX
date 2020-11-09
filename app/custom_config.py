from os import environ, path

'''
    Configuration class.
'''
class Config():
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    api_test = "/test"

class DevConfig(Config):
    PATH_CONFIG = './config/MS-Notifications-Dev.yaml'
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True

