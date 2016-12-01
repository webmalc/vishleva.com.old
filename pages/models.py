from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.db import models
from photologue.models import Gallery


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


