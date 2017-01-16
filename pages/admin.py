from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from .models import ExtendedFlatPage
from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery
from .models import GalleryExtended, Review
from reversion.admin import VersionAdmin
from ordered_model.admin import OrderedModelAdmin


@admin.register(Review)
class ReviewAdmin(VersionAdmin, OrderedModelAdmin):
    model = Review
    list_display = (
        'id', 'client', 'admin_thumbnail', 'created_at', 'is_enabled', 'move_up_down_links'
    )
    list_display_links = ('id', 'client')
    search_fields = (
         'id', 'text', 'client__last_name', 'client__first_name', 'client__phone', 'client__email'
    )
    list_filter = (('created_at', DateRangeFilter),)
    raw_id_fields = ['client', 'photo']
    fieldsets = (
        ('General', {
            'fields': ('text', 'client', 'photo')
        }),
        ('Configuration', {
            'classes': ('collapse',),
            'fields': ('is_enabled',)
        }),
    )


class GalleryExtendedInline(admin.StackedInline):
    model = GalleryExtended
    can_delete = False


class GalleryAdmin(GalleryAdminDefault):
    inlines = [GalleryExtendedInline, ]


class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = ExtendedFlatPage
        fields = '__all__'


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('keywords', 'description', 'registration_required', 'template_name'),
        }),
    )

    class Media:
        js = ('admin/js/pages.js',)


admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)
admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
