import requests

from django.conf import settings


class Ionic:
    headers = {'Authorization': 'Bearer ' + settings.IONIC_API_KEY}

    @classmethod
    def send_push(cls, text):
        response = requests.post(
            'https://api.ionic.io/push/notifications',
            headers=cls.headers,
            json={
                'profile': 'main',
                "send_to_all": True,
                'notification': {
                    'message': text
                }
            })
        return response
