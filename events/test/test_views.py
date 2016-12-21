from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from vishleva.lib.test import ViewTestCase
from events.models import Event
import arrow


class EventsViewTest(ViewTestCase):
    fixtures = ['tests/users.json', 'tests/events.json']

    def setUp(self):

        self.user = User.objects.get(pk=1)

    def test_admin_events_calendar_unauthorized_view(self):
        """
        Test payments list unauthorized view
        """
        self._test_unauthorized_view('admin:events_calendar')

    def test_calendar(self):
        """
        test calendar page
        """
        now = arrow.utcnow()
        event = Event()
        event.begin = now.replace(hours=+24).datetime
        event.end = now.replace(hours=+36).datetime
        event.title = 'test_title_now'
        event.status = 'open'
        event.save()

        self._login_superuser()
        url = reverse('admin:events_calendar')
        response = self.client.get(url)
        self._is_succesful(response, title='Events calendar | Django site admin')
        self.assertContains(response, 'test_title_now')

