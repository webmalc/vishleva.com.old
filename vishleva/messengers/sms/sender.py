from django.conf import settings
from django.utils.module_loading import import_string


class Sender(object):

    def __init__(self, **kwargs):
        self.sender = import_string(kwargs.get('sender_path', settings.SMS_SENDER))(kwargs.get('test'))

    def send_sms(self, message, phone=None, client=None):
        """
        Send sms via sms provider
        :param message: text
        :type message: string
        :param phone: phone
        :type phone: string
        :param client: client
        :type client: events.model.Client
        :return: send result
        :rtype: bool or dict
        """
        if not phone:
            phone = str(client.phone)
        if not phone:
            return False
        return self.sender.send(message, phone, client=client)
