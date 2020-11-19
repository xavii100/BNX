import abc

class Service(abc.ABC):

    @abc.abstractmethod
    def send_file(path, input_name):
        pass

    @abc.abstractmethod
    def orchestrate_file(path, file_name):
        pass