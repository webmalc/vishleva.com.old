from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Event, Client


@admin.register(Event)
class EventAdmin(VersionAdmin):
    model = Event
    list_display = (
        'id', 'title', 'begin', 'duration', 'total', 'is_paid', 'client', 'comment'
    )
    list_display_links = ('id', 'title')
    search_fields = (
        'id', 'title', 'comment', 'client__last_name', 'client__phone', 'client__email'
    )
    list_filter = ('begin', 'created_at')
    raw_id_fields = ['client']
    fieldsets = (
        ('General', {
            'fields': ('title', 'begin', 'end', 'comment')
        }),
        ('Calculation', {
            'fields': ('total', 'paid')
        }),
        ('Client', {
            'fields': ('client',)
        }),
    )

    class Media:
        js = ('js/admin/events.js',)


@admin.register(Client)
class ClientAdmin(VersionAdmin):
    model = Client
    list_display = (
        'id', 'last_name', 'first_name', 'patronymic', 'phone', 'email', 'comment'
    )
    list_display_links = ('id', 'last_name')
    search_fields = (
        'id', 'last_name', 'phone', 'email', 'comment'
    )
    list_filter = ('created_at', )
    fieldsets = (
        ('General', {
            'fields': ('first_name', 'last_name', 'patronymic', 'comment', 'gender')
        }),
        ('Contacts', {
            'fields': ('phone', 'email')
        }),
    )
