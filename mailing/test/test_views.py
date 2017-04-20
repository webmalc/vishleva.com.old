import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse

from vishleva.lib.test import ViewTestCase


class MailingViewTest(ViewTestCase):
    fixtures = ['tests/sms.json']

    def test_sms_api_without_key(self):
        """ Test sms list without key """
        url = reverse('mailing:sms_api_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sms_api(self):
        """ Test SMS API """
        url = reverse('mailing:sms_api_list')
        key = hashlib.md5(settings.API_KEY.encode('utf-8')).hexdigest()
        response = self.client.get(url + '?key=' + key)
        self.assertContains(response, 'test sms 1')
        self.assertContains(response, '+79253172878')
        self.assertContains(response, 'test sms 2')
        self.assertContains(response, '+79037356096')
        self.assertNotContains(response, 'test sms 3')
        self.assertNotContains(response, 'test sms 4')

        response = self.client.get(url + '?key=' + key)
        self.assertNotContains(response, 'test sms 1')
