from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTestCase(TestCase):

    def _test_unauthorized_view(self, route_name, redirect_route='admin:login', params={}):
        url = reverse(route_name, kwargs=params)
        redirect = reverse(redirect_route) + '?next=' + url
        response = self.client.get(url)
        self.assertEquals(response.url, redirect)
        self.assertEquals(response.status_code, 302)

    def _login_superuser(self):
        login = self.client.login(username='admin', password='password')
        self.assertEqual(login, True)

    def _is_succesful(self, response, title=None):
        """
        :param response: django response
        :param title: html title
        :type title: string or none
        """
        self.assertEqual(response.status_code, 200)
        if title:
            self.assertContains(response, title)


class FormTestCase(TestCase):
    pass


class TaskTestCase(TestCase):
    pass

