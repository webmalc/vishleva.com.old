from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.utils import timezone
from reversion.admin import VersionAdmin
from .models import Event, Client
from django.conf.urls import url
from django.template.response import TemplateResponse
from .lib.calendar import Calendar


@admin.register(Event)
class EventAdmin(VersionAdmin):
    model = Event
    change_list_template = 'admin/events/change_list.html'
    list_display = (
        'id', 'title', 'begin', 'duration', 'total', 'is_paid', 'client', 'status'
    )
    list_display_links = ('id', 'title')
    search_fields = (
        'id', 'title', 'comment', 'client__last_name', 'client__phone', 'client__email'
    )
    list_filter = (('begin', DateRangeFilter), 'status', ('created_at', DateRangeFilter))
    raw_id_fields = ['client']
    readonly_fields = ('notified_at',)
    fieldsets = (
        ('General', {
            'fields': ('title', 'begin', 'end', 'comment', 'status', 'google_calendar_id', 'notified_at')
        }),
        ('Calculation', {
            'fields': ('total', 'expenses', 'paid')
        }),
        ('Client', {
            'fields': ('client',)
        }),
    )

    def get_urls(self):
        return [
            url(r'^calendar/$', self.admin_site.admin_view(self.calendar_view), name='events_calendar')
        ] + super(EventAdmin, self).get_urls()

    def calendar_view(self, request):
        context = self.admin_site.each_context(request)
        context['title'] = 'Events calendar'
        calendar = Calendar()
        context['calendar'] = calendar
        context['days'] = calendar.get_days()
        context['year'] = timezone.now().strftime(format='%Y')
        context['hours'] = range(0, 24)
        return TemplateResponse(request, "admin/events/calendar.html", context)

    def changelist_view(self, request, extra_context=None):
        response = super(EventAdmin, self).changelist_view(request, extra_context)
        query_set = response.context_data["cl"].queryset
        extra_context = extra_context or {}
        extra_context['total'] = Event.objects.get_total(queryset=query_set)
        extra_context['expenses'] = Event.objects.get_expenses(queryset=query_set)
        extra_context['paid'] = Event.objects.get_paid(queryset=query_set)
        extra_context['result'] = extra_context['total'] - extra_context['expenses']
        return super(EventAdmin, self).changelist_view(request, extra_context=extra_context)

    class Media:
        js = ('js/admin/events.js', 'https://apis.google.com/js/client.js?onload=checkAuth')
        css = {
            'all': ('css/admin/events.css',)
        }


@admin.register(Client)
class ClientAdmin(VersionAdmin):
    model = Client
    list_display = (
        'id', 'last_name', 'first_name', 'patronymic', 'phone', 'email', 'social_url'
    )
    list_display_links = ('id', 'last_name', 'first_name')
    search_fields = (
        'id', 'last_name', 'phone', 'email', 'comment'
    )
    list_filter = ('created_at', )
    fieldsets = (
        ('General', {
            'fields': ('first_name', 'last_name', 'patronymic', 'comment', 'gender')
        }),
        ('Contacts', {
            'fields': ('phone', 'social_url', 'email')
        }),
    )
