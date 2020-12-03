
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
    def CONTENT_LANGUAGE(self):
        return self.__properties['content-language']

    @property
    def REJECTED_FOLDERS(self):
        return self.__properties['excluded-folders']

    @property
    def COMMON_FRAMEWORK_URI(self):
        return self.__properties['client']['Common-Framework']['uri']

    @property
    def COMMON_FRAMEWORK_PREFIX(self):
        return self.__properties['client']['Common-Framework']['prefix']

    @property
    def COMMON_FRAMEWORK_API(self):
        return self.__properties['client']['Common-Framework']['cf-api']

    @property
    def INBOX_PATH(self):
        return self.__properties['inbox-path']

    @property
    def ORCHESTRATE_API(self):
        return self.__properties['client']['Common-Framework']['orchestrate-api']

    @property
    def OUTBOX_PATH(self):
        return self.__properties['outbox-path']

    @property
    def TIME_WAITED(self):
        return self.__properties['time-waited']

    @property
    def UUID(self):
        return self.__properties['uuid']
