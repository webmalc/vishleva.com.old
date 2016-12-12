from django.core import mail
from vishleva.lib.test import TaskTestCase
from events.tasks import event_notifications_task
from django.conf import settings
from events.models import Event
from django.utils import timezone


class EventsTasksTest(TaskTestCase):
    fixtures = []

    def setUp(self):
        super(TaskTestCase, self).setUp()
        self.now = timezone.now()
        event = Event()
        event.begin = self.now + timezone.timedelta(hours=3)
        event.end = self.now + timezone.timedelta(hours=6)
        event.title = 'test_title_now'
        event.status = 'open'
        event.save()

    def test_event_notifications_task(self):
        """
        Test event_notifications_task
        """
        event_notifications_task.delay()
        self.assertEqual(len(mail.outbox), 1)
        event = Event.objects.first()
        self.assertEqual(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX + 'Upcoming event - ' + event.title)
        self.assertNotEqual(event.notified_at, None)

