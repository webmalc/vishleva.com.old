from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@tag('unit', 'view')
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


@tag('live')
class LiveTestCase(StaticLiveServerTestCase):
    fixtures = ['tests/users.json', 'tests/pages.json', 'tests/galleries.json']

    @classmethod
    def setUpClass(cls):
        super(LiveTestCase, cls).setUpClass()
        cls.selenium = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveTestCase, cls).tearDownClass()

    def _wait(self, wait_css_selector):
        WebDriverWait(self.selenium, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_css_selector))
        )

    def _login_as_superuser(self):
        self.selenium.get(self.live_server_url + '/admin/')
        username_field = self.selenium.find_element_by_id('id_auth-username')
        password_field = self.selenium.find_element_by_id('id_auth-password')
        username_field.send_keys('admin')
        password_field.send_keys('password')
        submit = self.selenium.find_element_by_css_selector('form button[type="submit"]')
        submit.click()


@tag('unit', 'form')
class FormTestCase(TestCase):
    pass


@tag('unit', 'task')
@override_settings(CELERY_ALWAYS_EAGER=True)
class TaskTestCase(TestCase):
    pass


@tag('unit', 'model')
class ModelTestCase(TestCase):
    pass


