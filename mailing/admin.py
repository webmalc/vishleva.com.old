from django.contrib import admin
from reversion.admin import VersionAdmin

from mailing.models import Sms


@admin.register(Sms)
class SmsAdmin(VersionAdmin):
    model = Sms
    list_display = ('id', 'phone', 'send_at', 'text', 'created_at')
    list_display_links = ('id', 'phone')
    search_fields = ('id', 'text', 'phone')
    readonly_fields = ('send_at', 'created_at')
    list_filter = ('created_at', 'send_at')
    fieldsets = (('General', {
        'fields': ('phone', 'text', 'send_at')
    }), ('Info', {
        'fields': ('send_at', 'created_at')
    }), )
