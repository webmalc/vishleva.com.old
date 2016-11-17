from django.db import models


class CommonInfo(models.Model):
    """ CommonInfo abstract model """

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    created_by = models.ForeignKey('django.contrib.auth.models.User', null=True, blank=True, on_delete=models.CASCADE,
                                   editable=False, related_name="%(app_label)s_%(class)s_created_by")
    modified_by = models.ForeignKey('django.contrib.auth.models', null=True, blank=True, on_delete=models.CASCADE,
                                    editable=False, related_name="%(app_label)s_%(class)s_modified_by")

    def __str__(self):
        return getattr(self, 'name', '{} #{}'.format(type(self).__name__, str(self.id)))

    class Meta:
        abstract = True


class CommentMixin(models.Model):
    comment = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
