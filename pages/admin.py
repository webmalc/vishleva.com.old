import io
import os
import zipfile

from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin
from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import PHOTOLOGUE_DIR, Gallery, Photo
from reversion.admin import VersionAdmin

from .models import ExtendedFlatPage, GalleryExtended, Review


@admin.register(Review)
class ReviewAdmin(VersionAdmin, OrderedModelAdmin):
    model = Review
    list_display = ('id', 'short_text', 'client', 'admin_thumbnail',
                    'created_at', 'is_enabled', 'move_up_down_links')
    list_display_links = ('id', 'short_text')
    search_fields = ('id', 'text', 'client__last_name', 'client__first_name',
                     'client__phone', 'client__email')
    list_filter = (('created_at', DateRangeFilter), )
    raw_id_fields = ['client', 'photo']
    fieldsets = (('General', {
        'fields': ('text', 'client', 'photo')
    }), ('Configuration', {
        'classes': ('collapse', ),
        'fields': ('is_enabled', )
    }), )


class GalleryExtendedInline(admin.StackedInline):
    model = GalleryExtended
    can_delete = False


class GalleryAdmin(GalleryAdminDefault):
    inlines = [
        GalleryExtendedInline,
    ]


class PhotoAdmin(PhotoAdminDefault):
    actions = ['export']

    def export(self, request, queryset):
        """
        Download selected files as ZIP
        """
        zip_subdir = 'photos'
        zip_filename = '{}.zip'.format(zip_subdir)
        zip_bytes = io.BytesIO()

        with zipfile.ZipFile(zip_bytes, "w") as zf:
            for photo in queryset.all():
                path = photo.image.path
                fdir, fname = os.path.split(path)
                zip_path = os.path.join(zip_subdir, fname)

                zf.write(path, zip_path)

        response = HttpResponse(
            zip_bytes.getvalue(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            zip_filename)

        return response

    export.short_description = 'Download photos'


class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = ExtendedFlatPage
        fields = '__all__'


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = ((None, {
        'fields': ('url', 'title', 'content', 'sites')
    }), (_('Advanced options'), {
        'classes': ('collapse', ),
        'fields':
        ('keywords', 'description', 'registration_required', 'template_name'),
    }), )

    class Media:
        js = ('admin/js/pages.js', )


admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)
admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)
