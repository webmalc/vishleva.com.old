from django.db import models
from django.conf import settings


class CommonInfo(models.Model):
    """ CommonInfo abstract model """

    AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                   editable=False, related_name="%(app_label)s_%(class)s_created_by")
    modified_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                    editable=False, related_name="%(app_label)s_%(class)s_modified_by")

    def __str__(self):
        return getattr(self, 'name', '{} #{}'.format(type(self).__name__, str(self.id)))

    class Meta:
        abstract = True


class CommentMixin(models.Model):
    comment = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True
