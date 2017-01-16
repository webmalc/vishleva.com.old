from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.db import models
from photologue.models import Gallery
from ordered_model.models import OrderedModel
from vishleva.models import CommonInfo


class GalleryExtended(models.Model):
    gallery = models.OneToOneField(Gallery, related_name='extended')
    small_description = models.TextField()

    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Extra fields'

    def __str__(self):
        return self.gallery.title


class ExtendedFlatPage(FlatPage):
    keywords = models.CharField(max_length=255, verbose_name=_('keywords'))
    description = models.CharField(max_length=255, verbose_name=_('description'))


class Review(OrderedModel, CommonInfo):
    """
    Client reviews
    """
    text = models.TextField(db_index=True)
    client = models.ForeignKey('events.Client')
    photo = models.ForeignKey('photologue.Photo', on_delete=models.SET_NULL, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)

    def admin_thumbnail(self):
        return self.photo.admin_thumbnail() if self.photo else None
    admin_thumbnail.short_description = _('Photo')
    admin_thumbnail.allow_tags = True

    def __str__(self):
        return "#{} review from {}".format(self.pk, self.client)

    class Meta(OrderedModel.Meta):
        pass


