from django.db import models
from django.core.validators import MinValueValidator
from vishleva.models import CommonInfo, CommentMixin
from phonenumber_field.modelfields import PhoneNumberField


class Event(CommonInfo, CommentMixin):
    """
    Event model
    """
    datetime = models.DateTimeField()
    title = models.CharField(max_length=255)
    total = total = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    is_paid = models.BooleanField(default=False)


class Client(CommonInfo, CommentMixin):
    """
    Client model
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(max_length=30)
    email = models.EmailField(max_length=200)
