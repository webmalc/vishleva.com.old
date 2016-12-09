from django.core import mail
from django.test import override_settings
from vishleva.lib.test import TaskTestCase
from vishleva.tasks import mail_managers_task
from django.conf import settings


class MainTasksTest(TaskTestCase):
    fixtures = []

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_mail_managers_task(self):
        """
        Test mail_managers_task
        """
        mail_managers_task.delay(
            subject='New message via contact form',
            template='emails/contact_form.html',
            data={'name': 'test name', 'contacts': 'test contacts', 'message': 'test message'}
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX + 'New message via contact form')

