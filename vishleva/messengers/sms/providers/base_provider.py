from abc import ABCMeta, abstractmethod


class BaseProvider(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, test=None):
        """ init """

    @abstractmethod
    def send(self, message, phone, client):
        """
        Send sms message
        """

    @abstractmethod
    def add(self, message, phone, client):
        """
        Add sms message for processing
        """

    @abstractmethod
    def process(self):
        """
        Process added messages
        """
