from app import log
from app.properties import Properties

'''
    Properties class.
'''
class PropertiesException(object):

    __instance = None
    __properties = None

    def __init__(self, yml = None):
        if PropertiesException.__instance != None:
            print("algo")
        else:
            PropertiesException.__instace = self
            if PropertiesException.__properties == None and yml is not None:
                PropertiesException.__properties = yml

    @property 
    def CONNECTION_TRR_ERROR_DETAILS(self):
        return self.__properties['connection-trr']['details']

    @property
    def CONNECTION_TRR_ERROR_LOCATION(self):
        return self.__properties['connection-trr']['location']

    @property
    def EXC_NOT_FILE_FOUND_DETAILS(self):
        return self.__properties['file-not-found']['details']

    @property
    def EXC_NOT_FILE_FOUND_LOCATION(self):
        return self.__properties['file-not-found']['location']   

    @property
    def EXC_NOT_INTERFACE_FOUND_DETAILS(self):
        return self.__properties['interface-not-found']['details']
        
    @property
    def EXC_NOT_INTERFACE_FOUND_LOCATION(self):
        return self.__properties['interface-not-found']['location']  

    @property
    def EXC_BAD_REQUEST_DETAILS(self):
        return self.__properties['bad-request']['details']
    
    @property
    def EXC_BAD_REQUEST_LOCATION(self):
        return self.__properties['bad-request']['location']
    
    @property
    def EXC_FORBIDDEN_DETAILS(self):
        return self.__properties['forbidden']['details']

    @property
    def EXC_FORBIDDEN_LOCATION(self):
        return self.__properties['forbidden']['location']
    
    @property
    def EXC_NOT_FOUND_DETAILS(self):
        return self.__properties['notFound']['details']

    @property
    def EXC_NOT_FOUND_LOCATION(self):
        return self.__properties['notFound']['location']
    
    @property
    def EXC_METHOD_NOT_ALLOWED_DETAILS(self):
        return self.__properties['methodNotAllowed']['details']
        
    @property
    def EXC_NO_DATABASE_CONECTION_DETAILS(self):
        return self.__properties['noDatabase']['details']

    @property
    def EXC_NO_DATABASE_CONECTION_LOCATION(self):
        return self.__properties['noDatabase']['location']

    @property
    def EXC_METHOD_NOT_ALLOWED_LOCATION(self):
        return self.__properties['methodNotAllowed']['location']
    
    @property
    def EXC_SERVER_ERROR_DETAILS(self):
        return self.__properties['serverError']['details']

    @property
    def EXC_SERVER_ERROR_LOCATION(self):
        return self.__properties['serverError']['location']

    @property
    def EXC_FILE_EMPTY_DETAILS(self):
        return self.__properties['fileName']['details']

    @property
    def EXC_FILE_EMPTY_LOCATION(self):
        return self.__properties['fileName']['location']
    
    @property
    def EXC_PATH_TYPE_DETAILS(self):
        return self.__properties['path']['type']['details']

    @property
    def EXC_PATH_TYPE_LOCATION(self):
        return self.__properties['path']['type']['location']
        
    @property
    def EXC_PATH_INVALID_DETAILS(self):
        return self.__properties['path']['invalid']['details']

    @property
    def EXC_PATH_INVALID_LOCATION(self):
        return self.__properties['path']['invalid']['location']

    @property
    def EXC_PATH_EMPTY_DETAILS(self):
        return self.__properties['path']['empty']['details']

    @property
    def EXC_PATH_EMPTY_LOCATION(self):
        return self.__properties['path']['empty']['location']

    @property
    def EXC_FILE_DATE_NOT_FOUND_DETAILS(self):
        return self.__properties['fileDate']['details']

    @property
    def EXC_FILE_DATE_NOT_FOUND_LOCATION(self):
        return self.__properties['fileDate']['location']

    @property
    def EXC_FILE_NOT_MOVED_DETAILS(self):
        return self.__properties['moveFile']['empty']['details']

    @property
    def EXC_FILE_NOT_MOVED_LOCATION(self):
        return self.__properties['moveFile']['empty']['location']

    @property
    def EXC_ACCEPT_EMPTY_DETAILS(self):
        return self.__properties['accept']['empty']['details']
    
    @property
    def EXC_ACCEPT_EMPTY_LOCATION(self):
        return self.__properties['accept']['empty']['location']
    
    @property
    def EXC_ACCEPT_TYPE_DETAILS(self):
        return self.__properties['accept']['mimeType']['details']
    
    @property
    def EXC_ACCEPT_TYPE_LOCATION(self):
        return self.__properties['accept']['mimeType']['location']

    @property
    def EXC_CONTENT_EMPTY_DETAILS(self):
        return self.__properties['contentType']['empty']['details']
    
    @property
    def EXC_CONTENT_EMPTY_LOCATION(self):
        return self.__properties['contentType']['empty']['location']
    
    @property
    def EXC_CONTENT_TYPE_DETAILS(self):
        return self.__properties['contentType']['mimeType']['details']
    
    @property
    def EXC_CONTENT_TYPE_LOCATION(self):
        return self.__properties['contentType']['mimeType']['location']
    
    @property
    def EXC_UUID_EMPTY_DETAILS(self):
        return self.__properties['uuid']['empty']['details']

    @property
    def EXC_UUID_EMPTY_LOCATION(self):
        return self.__properties['uuid']['empty']['location']
    
    @property
    def EXC_CONTENT_LANGUAGE_EMPTY_DETAILS(self):
        return self.__properties['contentLanguage']['empty']['details']
    
    @property
    def EXC_CONTENT_LANGUAGE_EMPTY_LOCATION(self):
        return self.__properties['contentLanguage']['empty']['location']
    
    @property
    def EXC_CONTENT_LANGUAGE_TYPE_DETAILS(self):
        return self.__properties['contentLanguage']['format']['details']
    
    @property
    def EXC_CONTENT_LANGUAGE_TYPE_LOCATION(self):
        return self.__properties['contentLanguage']['format']['location']

    