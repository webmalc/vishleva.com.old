from django.views.generic import TemplateView
from .models import ExtendedFlatPage


class MainView(TemplateView):
    """
    Main page
    """
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['about'] = ExtendedFlatPage.objects.all().filter(url='/about/').first()
        return context
