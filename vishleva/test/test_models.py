from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import override_settings

from events.models import Client
from mailing.models import Sms
from vishleva.lib.test import ModelTestCase
from vishleva.messengers.mailer import Mailer
from vishleva.messengers.sms.sender import Sender


class MailerTest(ModelTestCase):
    fixtures = ['tests/users.json', 'tests/events.json']
    phone = '+79253172873'
    text = 'test message text'

    def test_mail_user(self):
        subject = 'Test user message'
        user = User.objects.first()
        Mailer.mail_user(subject, 'emails/base.html',
                         {'content': 'test content'}, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user, mail.outbox[0].recipients())
        self.assertEqual(mail.outbox[0].subject,
                         settings.EMAIL_SUBJECT_PREFIX + subject)

    def _test_sms_sender(self):
        """ universal test for sms sender """
        sender = Sender(test=True)
        client = Client.objects.get(pk=1)
        result = sender.send_sms(self.text, client=client)
        self.assertTrue(result['result'])

        result = sender.send_sms(self.text, phone=self.phone)
        self.assertTrue(result['result'])
        return sender

    @override_settings(SMS_SENDER='vishleva.messengers.sms.providers.db.Db')
    def test_db_sms_sender(self):
        sender = self._test_sms_sender()

        sms = Sms.objects.get(phone=self.phone, text=self.text)
        self.assertTrue(sms)
        sms = Sms.objects.get(client__id=1)
        self.assertTrue(sms)

        Sms.objects.all().delete()
        sender.add_sms(self.text + '1', self.phone)
        sender.add_sms(self.text + '2', self.phone)
        sender.process()
        sms_objects = Sms.objects.all().order_by('text')
        self.assertEqual(2, len(sms_objects))
        self.assertEqual([self.text + '1', self.text + '2'],
                         [m.text for m in sms_objects])

    @override_settings(
        SMS_SENDER='vishleva.messengers.sms.providers.epochta.Epochta')
    def test_epochta_sms_sender(self):
        self._test_sms_sender()
