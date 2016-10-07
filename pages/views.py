from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from .models import ExtendedFlatPage
from .forms import ContactForm
from vishleva.messengers.mailer import Mailer


class MainView(TemplateView):
    """
    Main page
    """
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['about'] = ExtendedFlatPage.objects.all().filter(url='/about/').first()
        context['form'] = ContactForm()
        return context


def send_email(request):
    """
    Send email from contact form
    :param request: django.http.HttpRequest
    :type request: django.http.HttpRequest
    :return: response
    :rtype: django.http.JsonResponse
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Mailer.mail_managers(
                subject=_('New message from user'),
                template='emails/contact_form.html',
                data=form.cleaned_data
            )
            return JsonResponse({'success': True, 'message': _('Your message was successfully sent')})

    return JsonResponse({
        'success': False,
        'message': _('Sorry! Error while sending message! Please refresh the page and try again')
    })
