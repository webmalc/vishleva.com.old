from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from vishleva.lib.test import ViewTestCase
from pages.models import ExtendedFlatPage


class PageViewTest(ViewTestCase):
    fixtures = ['tests/users.json', 'tests/pages.json', 'tests/galleries.json']

    def setUp(self):

        self.user = User.objects.get(pk=1)

    def test_admin_unauthorized_view(self):
        """
        Test payments list unauthorized view
        """
        self._test_unauthorized_view('admin:index')

    def test_index(self):
        """
        test main page
        """
        url = reverse('index')
        response = self.client.get(url)
        self._is_succesful(response, title='Фотограф Александра Вишлева - профессиональный фотограф Москва')
        self.assertContains(response, 'id="works"')
        self.assertContains(response, 'about content')
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, 'prices content')
        self.assertContains(response, 'extrahead content')

    def test_special_on(self):
        """
        test special content enabled
        """
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, 'special content')

    def test_special_off(self):
        """
        test special content disabled
        """
        special = ExtendedFlatPage.objects.all().filter(url='/special/').first()
        special.delete()
        url = reverse('index')
        response = self.client.get(url)
        self.assertNotContains(response, 'special content')

    def test_gallery_display(self):
        """
        test gallery display
        """
        # TODO: complete
        self.assertTrue(False)
