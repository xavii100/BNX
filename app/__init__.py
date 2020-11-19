from app import custom_config
from app.properties import Properties
import yaml
import os

def create_app():    
    os.environ["ENVIRONMENT"] = "DEV"
    env = os.environ.get('ENVIRONMENT')

    config = __custom_config(env)
    path = config.PATH_CONFIG
    
    yml = init_properties(path)
    Properties(yml)

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