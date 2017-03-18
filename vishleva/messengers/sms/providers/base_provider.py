from abc import ABCMeta, abstractmethod


class BaseProvider(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, test=None):
        """ init """

    @abstractmethod
    def send(self, message, phone):
        """
        Send sms message
        :param message: message
        :type message: str
        :param phone: phone
        :type phone: str
        :return: send result
        :rtype: dict
        """
