from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Event, Client


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
    list_filter = ('begin', 'status', 'created_at')
    raw_id_fields = ['client']
    fieldsets = (
        ('General', {
            'fields': ('title', 'begin', 'end', 'comment', 'status', 'google_calendar_id')
        }),
        ('Calculation', {
            'fields': ('total', 'expenses', 'paid')
        }),
        ('Client', {
            'fields': ('client',)
        }),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total'] = Event.objects.get_total(with_expenses=True)
        extra_context['paid'] = Event.objects.get_paid()
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
