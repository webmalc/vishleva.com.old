from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User
from vishleva.lib.test import ModelTestCase
from vishleva.messengers.mailer import Mailer


class MailerTest(ModelTestCase):
    fixtures = ['tests/users.json']

    def test_mail_user(self):
        subject = 'Test user message'
        user = User.objects.first()
        Mailer.mail_user(subject, 'emails/base.html', {'content': 'test content'}, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user, mail.outbox[0].recipients())
        self.assertEqual(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX + subject)


