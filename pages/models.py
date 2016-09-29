from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class ExtendedFlatPage(FlatPage):
    keywords = models.CharField(max_length=255, verbose_name=_('keywords'))
    description = models.CharField(max_length=255, verbose_name=_('description'))


