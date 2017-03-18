from .base_provider import BaseProvider


class Db(BaseProvider):
    """ Save sms in database """

    def __init__(self, test=None):
        self.test = test

    def send(self, message, phone):
        pass
