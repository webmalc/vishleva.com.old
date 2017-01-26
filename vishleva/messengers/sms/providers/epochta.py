import requests
import hashlib
from django.conf import settings
from .base_provider import BaseProvider


class Epochta(BaseProvider):

    base_url = 'http://atompark.com/api/sms/3.0/'
    public_key = settings.EPOCHTA_PUBLIC_KEY
    private_key = settings.EPOCHTA_PRIVATE_KEY
    sender = 'VISHLEVA'
    test = settings.DEBUG
    version = '3.0'

    def __init__(self, test=None):
        if test:
            self.test = test

    def send(self, message, phone):
        data = {'text': message, 'phone': phone, 'sender': self.sender}
        response = self._send_request('sendSMS', data)
        return response

    def _send_request(self, method, data):
        url = self.base_url + method
        data['key'] = self.public_key
        if self.test:
            data['test'] = 1
        data['sum'] = self._signature(action=method, params=data)
        response = requests.post(url, data=data)
        json = response.json()
        if 'error' in response.json():
            raise RuntimeError('Epochta error! {error} Code: {code}'.format(**json))
        return json

    def _signature(self, action, params):
        params['version'] = self.version
        params['action'] = action
        return hashlib.md5(
            (''.join([str(params[k]) for k in sorted(params.keys())]) + self.private_key).encode('utf-8')
        ).hexdigest()

