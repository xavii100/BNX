from app import log
from app.properties import Properties

'''
    Properties class.
'''
class PropertiesLog(object):

    __instance = None
    __properties = None

    def __init__(self, yml = None):
        if PropertiesLog.__instance != None:
            print("algo")
        else:
            PropertiesLog.__instace = self
            if PropertiesLog.__properties == None and yml is not None:
                PropertiesLog.__properties = yml
    
    @property
    def CONTROLLER_INFO_HEADER(self):
        return self.__properties['info']['controller']['headers']
    
    @property
    def CONTROLLER_INFO_REQUEST(self):
        return self.__properties['info']['controller']['request']

    @property
    def ERROR_EXCEPTION_HANDLER(self):
        return self.__properties['error']['exception_handler']
