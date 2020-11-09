from app.exception_handler import exception as error_blueprint
from app.controller import notifications as main_blueprint    
from app.properties_exc import PropertiesException
from app.properties_log import PropertiesLog
from app.properties import Properties
from app.log import log
from flask import Flask
import yaml

'''
    Function to create app with an specific env.
'''
def create_app(env = 'Dev'):
    app = Flask(__name__)
    
    app.config.from_object('app.custom_config.'+env+'Config')
    path = app.config['PATH_CONFIG']

    yml = init_properties(path)
    
    Properties(yml['properties'])
    PropertiesException(yml['exception'])    
    PropertiesLog(yml['log'])

    app.register_blueprint(error_blueprint)
    app.register_blueprint(main_blueprint)
        
    return app

def init_properties(path_config):
   with open (path_config) as file: 
        return yaml.load(file, Loader=yaml.FullLoader)