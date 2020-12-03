
from app import custom_config
from app.properties import Properties
from flask import Flask
import yaml
import os

def create_app():    
    app = Flask(__name__)

    if "ENVIRONMENT" in os.environ:
        env = os.environ.get('ENVIRONMENT')
    else:
        env = 'DEV'

    config = __custom_config(env)
    path = config.PATH_CONFIG
    
    yml = init_properties(path)
    Properties(yml)


    return app

def __custom_config(env):
    if env == 'DEV':
        return custom_config.DEVConfig()
    if env == 'SIT':
        return custom_config.SITConfig()
    if env == 'UAT':
        return custom_config.UATConfig()
    if env == 'PROD':
        return custom_config.PRODConfig()


def init_properties(path_config):
   with open (path_config) as file: 
        return yaml.load(file, Loader=yaml.FullLoader)