from vishleva.lib.test import FormTestCase
from pages.forms import ContactForm


class PageFormsTest(FormTestCase):
    fixtures = []

    def test_contact_form_invalid(self):
        """
        Test contact form: invalid
        """
        form = ContactForm({
            'name': 'test' * 1000
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_valid(self):
        """
        Test contact form: valid
        """
        form = ContactForm({
            'name': 'test' * 10,
            'contacts': 'test contacts',
            'message': 'test message'
        })
        self.assertTrue(form.is_valid())
