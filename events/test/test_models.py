from vishleva.lib.test import ModelTestCase
from events.models import Event, Client


class EventModelTest(ModelTestCase):
    fixtures = ['tests/events.json']

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

