from mailing.models import Sms

from .base_provider import BaseProvider


class Db(BaseProvider):
    """ Save sms in database """

    def __init__(self, test=None):
        self.test = test
        self.storage = []

    def send(self, message, phone, client):
        sms = Sms.create(phone, message)
        sms.client = client
        sms.save()
        return {'result': sms}

    def add(self, message, phone, client):
        sms = Sms.create(phone, message)
        sms.client = client
        self.storage.append(sms)

    def process(self):
        Sms.objects.bulk_create(self.storage)
