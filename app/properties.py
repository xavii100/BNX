import os

'''
    Properties class.
'''
class Properties(object):

    __instance = None
    __properties = None

    def __init__(self, yml = None):
        if Properties.__instance != None:
            print("algo")
        else:
            Properties.__instace = self
            if Properties.__properties == None and yml is not None:
                Properties.__properties = yml

    @property
    def ACCEPT(self):
        return self.__properties['accept']['name']

    @property
    def CONTENT(self):
        return self.__properties['contentType']['name']

    @property
    def CONTENT_LANGUAGE(self):
        return self.__properties['contentLanguage']['name']

    @property
    def REQUEST_FORMAT(self):
        return self.__properties['controller']['format']
        
    @property
    def RESPONSE_FORMAT(self):
        return self.__properties['controller']['response']['format']

    @property
    def SUCCESS(self):
        return self.__properties['success']
    
    @property
    def URL_PREFIX(self):
        uri = os.environ.get('SUFFIX')
        if uri is not None:
            return uri
        else: 
            return '/api/v1'

    @property
    def UUID(self):
        return self.__properties['uuid']['name']