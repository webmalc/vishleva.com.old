from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import override_settings

from events.models import Client
from vishleva.lib.test import ModelTestCase
from vishleva.messengers.mailer import Mailer
from vishleva.messengers.sms.sender import Sender


class MailerTest(ModelTestCase):
    fixtures = ['tests/users.json', 'tests/events.json']

    def test_mail_user(self):
        subject = 'Test user message'
        user = User.objects.first()
        Mailer.mail_user(subject, 'emails/base.html',
                         {'content': 'test content'}, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user, mail.outbox[0].recipients())
        self.assertEqual(mail.outbox[0].subject,
                         settings.EMAIL_SUBJECT_PREFIX + subject)

    @override_settings(SMS_SENDER='vishleva.messengers.sms.providers.db.Db')
    def test_db_sms_sender(self):
        self.assertTrue(False)

    @override_settings(
        SMS_SENDER='vishleva.messengers.sms.providers.epochta.Epochta')
    def test_epochta_sms_sender(self):
        sender = Sender(test=True)
        client = Client.objects.get(pk=1)
        text = 'test message'
        result = sender.send_sms(text, client=client)
        self.assertTrue(result['result'])

        result = sender.send_sms(text, phone='+79037356096')
        self.assertTrue(result['result'])
