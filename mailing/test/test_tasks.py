from django.conf import settings
from django.core import mail
from mailing.tasks import new_sms_notifications_task
from vishleva.lib.test import TaskTestCase


class SmsTasksTest(TaskTestCase):
    fixtures = ['tests/sms.json']

    def test_new_sms_notifications_task(self):
        """
        Test test_sms_notifications
        """
        new_sms_notifications_task.delay()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         settings.EMAIL_SUBJECT_PREFIX + 'New sms waiting')
