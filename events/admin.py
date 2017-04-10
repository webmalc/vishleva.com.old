from datetime import datetime

from daterange_filter.filter import DateRangeFilter
from django.conf.urls import url
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView
from events.forms import SmsForm
from reversion.admin import VersionAdmin
from vishleva.messengers.sms.sender import Sender

from .lib.calendar import Calendar
from .models import Client, Event


class EventClosedFilter(admin.SimpleListFilter):
    title = _('Filter closed')
    parameter_name = 'closed'

    def lookups(self, request, model_admin):
        return ((None, _('Yes')), ('show', _('No')), )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected':
                self.value() == lookup,
                'query_string':
                cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display':
                title,
            }

    def queryset(self, request, queryset):
        if self.value() != 'show':
            return queryset.exclude(status='closed')


@admin.register(Event)
class EventAdmin(VersionAdmin):
    model = Event
    change_list_template = 'admin/events/change_list.html'
    list_display = ('id', 'title', 'begin', 'duration', 'total', 'is_paid',
                    'client', 'status')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'comment', 'client__last_name',
                     'client__first_name', 'client__phone', 'client__email')
    list_filter = (('begin', DateRangeFilter), EventClosedFilter, 'status',
                   ('created_at', DateRangeFilter))
    raw_id_fields = ['client']
    readonly_fields = ('notified_at', )
    fieldsets = (('General', {
        'fields': ('title', 'begin', 'end', 'comment', 'status',
                   'google_calendar_id', 'notified_at')
    }), ('Calculation', {
        'fields': ('total', 'expenses', 'paid')
    }), ('Client', {
        'fields': ('client', )
    }), )

    def get_urls(self):
        """
        Additional events urls
        :return:
        :rtype:
        """
        return [
            url(r'^calendar/$',
                self.admin_site.admin_view(self.calendar_view),
                name='events_calendar')
        ] + super(EventAdmin, self).get_urls()

    def calendar_view(self, request):
        """
        Events calendar view
        :param request:
        :type request:
        :return:
        :rtype:
        """
        context = self.admin_site.each_context(request)
        context['title'] = 'Events calendar'
        calendar = Calendar(
            begin=request.GET.get('begin'), end=request.GET.get('end'))
        context['calendar'] = calendar
        context['days'] = calendar.get_days()
        context['year'] = timezone.now().strftime(format='%Y')
        context['hours'] = range(0, 24)
        return TemplateResponse(request, "admin/events/calendar.html", context)

    def get_changeform_initial_data(self, request):
        initial = super(EventAdmin, self).get_changeform_initial_data(request)
        begin_date = request.GET.get('begin_date')
        begin_time = request.GET.get('begin_time')
        end_date = request.GET.get('end_date')
        end_time = request.GET.get('end_time')
        try:
            initial['begin'] = datetime.strptime(
                begin_date + ' ' + begin_time,
                '%Y-%m-%d %H:%M:%S') if begin_date and begin_time else None
            initial['end'] = datetime.strptime(
                end_date + ' ' + end_time,
                '%Y-%m-%d %H:%M:%S') if end_date and end_time else None
        except ValueError:
            pass
        return initial

    def changelist_view(self, request, extra_context=None):
        response = super(EventAdmin, self).changelist_view(request,
                                                           extra_context)
        query_set = response.context_data["cl"].queryset
        extra_context = extra_context or {}
        extra_context['total'] = Event.objects.get_total(queryset=query_set)
        extra_context['expenses'] = Event.objects.get_expenses(
            queryset=query_set)
        extra_context['paid'] = Event.objects.get_paid(queryset=query_set)
        extra_context['result'] = extra_context['total'] - extra_context[
            'expenses']
        return super(EventAdmin, self).changelist_view(
            request, extra_context=extra_context)

    class Media:
        js = ('js/admin/events.js',
              'https://apis.google.com/js/client.js?onload=checkAuth')
        css = {'all': ('css/admin/events.css', )}


@admin.register(Client)
class ClientAdmin(VersionAdmin):
    model = Client
    list_display = ('id', 'last_name', 'first_name', 'patronymic', 'comment',
                    'phone', 'email')

    list_display_links = ('id', 'last_name', 'first_name')
    search_fields = ('id', 'last_name', 'phone', 'email', 'comment')
    list_filter = ('created_at', )
    actions = ['send_sms']
    fieldsets = (('General', {
        'fields':
        ('first_name', 'last_name', 'patronymic', 'comment', 'gender')
    }), ('Contacts', {
        'fields': ('phone', 'social_url', 'email')
    }), )

    def send_sms(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('{}?ids={}'.format(
            reverse_lazy('admin:send_sms'), ','.join(selected)))

    def get_urls(self):
        """
        Additional clients urls
        """
        return [
            url(r'^send/sms$',
                self.admin_site.admin_view(SmsView.as_view()),
                name='send_sms')
        ] + super(ClientAdmin, self).get_urls()


class SmsView(FormView):
    template_name = 'admin/events/sms.html'
    form_class = SmsForm
    success_url = reverse_lazy('admin:events_client_changelist')

    def get_initial(self):
        initial = super(SmsView, self).get_initial()
        initial['clients'] = self.request.GET.get('ids').split(',')
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        sender = Sender()
        for client in data['clients']:
            sender.add_sms(data['message'], client=client)
        sender.process()
        messages.add_message(self.request, messages.INFO,
                             'Sms`s saved to mailing list')
        return super(SmsView, self).form_valid(form)
