from vishleva.lib.test import ModelTestCase
from events.models import Event, Client
from django.utils import timezone
from events.lib.calendar import Calendar
from django.conf import settings
import pytz
import arrow


class EventModelTest(ModelTestCase):
    fixtures = ['tests/events.json']

    def test_get_for_notification(self):
        date = timezone.datetime(2016, 12, 8, 10, 0, 0, 0, pytz.UTC)
        queryset = Event.objects.get_for_notification(date)
        self.assertGreater(queryset.count(), 0)
        for event in queryset:
            self.assertTrue(event.begin >= date)
            self.assertTrue(event.notified_at is None)

    def test_events_total(self):
        manager = Event.objects
        self.assertEqual(33580, manager.get_total())
        self.assertEqual(32530, manager.get_total(with_expenses=True))
        self.assertEqual(25500, manager.get_total(queryset=manager.filter(status='open')))
        self.assertEqual(24450, manager.get_total(queryset=manager.filter(status='open'), with_expenses=True))

    def test_events_paid(self):
        manager = Event.objects
        self.assertEqual(2000, manager.get_paid())

    def test_client_to_str(self):
        client = Client.objects.get(last_name='Ivanov')
        self.assertEquals('Ivanov Sergey Ivanovich', str(client))

    def test_calendar(self):
        calendar = Calendar()
        now = arrow.now().floor('day').to('UTC').datetime
        week = now + timezone.timedelta(days=settings.EVENTS_CALENDAR_PERIOD)
        self.assertEqual(now, calendar.begin)
        self.assertEqual(week, calendar.end)

        event = Event()
        event.begin = now + timezone.timedelta(days=3)
        event.end = now + timezone.timedelta(days=4)
        event.title = 'test_title_now'
        event.status = 'open'
        event.save()

        days = calendar.get_days()
        self.assertEqual(settings.EVENTS_CALENDAR_PERIOD, len(days))

        for element in days:
            if event.begin <= element.date <= event.end:
                self.assertIn(event, element.events)
            for hour in element.hours:
                if event.begin <= hour.date <= event.end:
                    self.assertIn(event, hour.events)



