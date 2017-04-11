import arrow
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from events.models import Event
from mailing.models import Sms
from vishleva.lib.test import LiveTestCase, ViewTestCase


class EventsViewTest(ViewTestCase):
    fixtures = ['tests/users.json', 'tests/events.json']

    def setUp(self):

        self.user = User.objects.get(pk=1)

    def test_admin_events_calendar_unauthorized_view(self):
        """
        Test payments list unauthorized view
        """
        self._test_unauthorized_view('admin:events_calendar')

    def test_admin_sms_form(self):
        """ Test batch sms send to clients """
        self._login_superuser()
        url = reverse('admin:send_sms')
        response = self.client.get(url + '?ids=1,2,3')
        self.assertContains(response, 'id="id_message"')
        form = response.context['form']
        data = form.initial
        text = 'test sms message from form'
        data['message'] = text
        response = self.client.post(url + '?ids=1,2,3', data)
        sms = Sms.objects.all()
        self.assertEqual(3, len(sms))
        self.assertEqual(text, sms[0].text)

    def test_calendar(self):
        """
        Test calendar page
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
        self._is_succesful(
            response, title='Events calendar | Django site admin')
        self.assertContains(response, 'test_title_now')
        self.assertContains(
            response, 'events-calendar-date">' + now.format('D MMM').lower())

    def test_calendar_with_params(self):
        """
        Test calendar page with params
        """
        now = arrow.utcnow()
        period = settings.EVENTS_CALENDAR_PERIOD
        tag = 'events-calendar-date">'
        self._login_superuser()
        url = reverse('admin:events_calendar')

        # test end query
        response = self.client.get(
            "{}?end={}".format(url, now.format('YYYY-MM-DD')))
        self.assertNotContains(response, tag + now.format('D MMM').lower())
        self.assertContains(
            response, tag + now.replace(days=-period).format('D MMM').lower())
        self.assertNotContains(
            response,
            tag + now.replace(days=-(period + 1)).format('D MMM').lower())

        # test begin query
        end = now.replace(days=+period)
        response = self.client.get(
            "{}?begin={}".format(url, end.format('YYYY-MM-DD')))
        self.assertNotContains(response, tag + now.format('D MMM').lower())
        self.assertContains(response, tag + end.format('D MMM').lower())
        self.assertNotContains(
            response, tag + end.replace(days=-1).format('D MMM').lower())


class EventsLiveTests(LiveTestCase):
    def test_calendar(self):
        """
        Test calendar page
        """
        now = arrow.utcnow()
        tomorrow = now.replace(days=+1)
        begin_time = '02:00:00'
        end_time = '14:00:00'
        event = Event()
        event.begin = now.replace(hours=+24).datetime
        event.end = now.replace(hours=+36).datetime
        event.title = 'test_title_now'
        event.status = 'open'
        event.save()

        self._login_as_superuser()
        url = reverse('admin:events_calendar')
        self.selenium.get(self.live_server_url + url)

        assert 'test_title_now' in self.selenium.page_source
        assert 'events-calendar-date">' + now.format(
            'D MMM').lower() in self.selenium.page_source

        begin = self.selenium.find_element_by_css_selector(
            'td[data-time="{}"][data-date="{}"]'.format(
                begin_time, now.format('YYYY-MM-DD')))
        begin.click()
        end = self.selenium.find_element_by_css_selector(
            'td[data-time="{}"][data-date="{}"]'.format(
                end_time, tomorrow.format('YYYY-MM-DD')))
        end.click()

        assert now.format('YYYY-MM-DD') == self.selenium.find_element_by_id(
            'id_begin_0').get_attribute('value')
        assert begin_time == self.selenium.find_element_by_id(
            'id_begin_1').get_attribute('value')
        assert tomorrow.format(
            'YYYY-MM-DD') == self.selenium.find_element_by_id(
                'id_end_0').get_attribute('value')
        assert end_time == self.selenium.find_element_by_id(
            'id_end_1').get_attribute('value')
