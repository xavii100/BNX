from os import environ, path

'''
    Configuration class.
'''
class Config():
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    api_test = "/test"

class DEVConfig(Config):
    PATH_CONFIG = './config/MS-Listener-DEV.yaml'
    PATH_MSG = './config/Messages-{0}.yaml'
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

class SITConfig(Config):
    PATH_CONFIG = './config/MS-Listener-SIT.yaml'
    PATH_MSG = './config/Messages-{0}.yaml'
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

class UATConfig(Config):
    PATH_CONFIG = './config/MS-Listener-UAT.yaml'
    PATH_MSG = './config/Messages-{0}.yaml'
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class PRODConfig(Config):
    PATH_CONFIG = './config/MS-Listener-PROD.yaml'
    PATH_MSG = './config/Messages-{0}.yaml'
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
