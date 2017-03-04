from django.views.generic import TemplateView, CreateView, ListView
from django.conf import settings
from datetime import date
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from .models import ExtendedFlatPage, Review
from .forms import ContactForm, ClientReviewForm
from photologue.models import Gallery
from photologue.views import GalleryDetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vishleva.tasks import mail_managers_task
from vishleva.views import AjaxableResponseMixin


class GalleryView(GalleryDetailView):
    """
    Gallery vie
    """
    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        paginator = Paginator(self.object.photos.all(), settings.PHOTOS_PER_PAGE)
        page = self.kwargs.get('page', 1)
        try:
            context['photos'] = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            context['photos'] = paginator.page(1)

        return context


class MainView(TemplateView):
    """
    Main page
    """
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):

        days = (date.today() - settings.SITE_START_DATE).days
        context = super(MainView, self).get_context_data(**kwargs)
        context['days'] = days
        context['clients'] = days // 3
        context['orders'] = days // 4
        context['photos'] = days * 12 + date.today().weekday()
        context['about'] = ExtendedFlatPage.objects.all().filter(url='/about/').first()
        context['prices'] = ExtendedFlatPage.objects.all().filter(url='/prices/').first()
        context['specials'] = ExtendedFlatPage.objects.all().filter(url__startswith='/special')
        context['extrahead'] = ExtendedFlatPage.objects.all().filter(url='/extrahead/').first()
        context['form'] = ContactForm()
        context['galleries'] = Gallery.objects.on_site().is_public().order_by('-extended__order') #.exclude(slug__startswith='special')
        context['reviews'] = Review.objects.filter(is_enabled=True)[0:20]

        return context


class CreateReview(AjaxableResponseMixin, CreateView):
    """
    Create review (frontend)
    """
    model = Review
    form_class = ClientReviewForm

    def form_valid(self, form):
        review = form.save(commit=False)
        review.text += "\n\nClient contacts: {}" . format(form.cleaned_data['contacts'])
        review.is_enabled = False
        review.save()

        mail_managers_task.delay(
            subject=_('New client review.'),
            template='emails/client_review_manager.html',
            data={'review': review.text}
        )
        return JsonResponse({'message': 'Отзыв успешно добавлен. Он появится на сайте в ближайшее время.'})


class ReviewList(ListView):
    """
    All reviews 
    """
    model = Review
    queryset = Review.objects.filter(is_enabled=True)
    paginate_by = 30


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
            mail_managers_task.delay(
                subject=_('New message via contact form'),
                template='emails/contact_form.html',
                data=form.cleaned_data
            )
            return JsonResponse({'success': True, 'message': _('Your message was successfully sent')})

    return JsonResponse({
        'success': False,
        'message': _('Sorry! Error while sending message! Please refresh the page and try again')
    })
