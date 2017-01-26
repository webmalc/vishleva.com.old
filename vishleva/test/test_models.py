from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User
from vishleva.lib.test import ModelTestCase
from vishleva.messengers.mailer import Mailer
from vishleva.messengers.sms.sender import Sender
from events.models import Client


class MailerTest(ModelTestCase):
    fixtures = ['tests/users.json', 'tests/events.json']

    def test_mail_user(self):
        subject = 'Test user message'
        user = User.objects.first()
        Mailer.mail_user(subject, 'emails/base.html', {'content': 'test content'}, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user, mail.outbox[0].recipients())
        self.assertEqual(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX + subject)

    def test_sms_sender(self):
        sender = Sender(test=True)
        client = Client.objects.get(pk=1)
        text = 'test message'
        result = sender.send_sms(text, client=client)
        self.assertTrue(result['result'])

        result = sender.send_sms(text, phone='+79037356096')
        self.assertTrue(result['result'])

        self.assertRaises(RuntimeError, sender.send_sms, text, 'adads')

