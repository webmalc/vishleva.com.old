from django.db import models
from django.conf import settings


class NullableEmailField(models.EmailField):
    """
        Subclass of the EmailField that allows empty strings to be stored as NULL.
    """

    description = "EmailField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection, contex):
        """
        Gets value right out of the db and changes it if its ``None``.
        """
        if value is None:
            return ''
        else:
            return value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its ``None``.
        """
        if isinstance(value, models.EmailField):
            return value
        if value is None:
            return ''
        return value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """
        if value is '':
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value


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
