from django.db import models
from django.core.validators import MinValueValidator
from vishleva.models import CommonInfo, CommentMixin
from phonenumber_field.modelfields import PhoneNumberField


class Event(CommonInfo, CommentMixin):
    """
    Event model
    """
    begin = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=255)
    total = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    paid = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    client = models.ForeignKey('Client', null=True, blank=True, on_delete=models.SET_NULL, related_name="events")

    @property
    def is_paid(self):
        return self.total - self.paid <= 0


class Client(CommonInfo, CommentMixin):
    """
    Client model
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(max_length=30)
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
