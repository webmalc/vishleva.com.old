from django.db import models
from django.template.defaultfilters import pluralize
from django.utils import timezone
from django.core.validators import MinValueValidator
from vishleva.models import CommonInfo, CommentMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError


class Event(CommonInfo, CommentMixin):
    """
    Event model
    """
    begin = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    total = models.PositiveIntegerField(default=0, db_index=True, validators=[MinValueValidator(0)])
    paid = models.PositiveIntegerField(default=0, db_index=True, validators=[MinValueValidator(0)])
    client = models.ForeignKey('Client', null=True, blank=False, on_delete=models.SET_NULL, related_name="events")

    def is_paid(self):
        return self.total - self.paid <= 0
    is_paid.boolean = True

    def duration(self):
        duration = self.end - self.begin
        seconds = duration.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return '{} day{} {} hour{} {} minute{}'.format(
            duration.days,
            pluralize(duration.days),
            hours,
            pluralize(hours),
            minutes,
            pluralize(minutes)
        )

    def __str__(self):
        return '{} - {}. {}'.format(
            timezone.localtime(self.begin).strftime('%d %B %Y %H:%M'),
            self.duration(),
            self.title
        )

    def clean(self):
        if self.begin and self.end:
            if self.begin >= self.end:
                raise ValidationError('End ({}) must be greater than begin ({})'.format(
                    self.end.strftime('%d %B %Y %H:%M'), self.begin.strftime('%d %B %Y %H:%M')
                ))
            query = Event.objects.filter(begin__lt=self.end, end__gt=self.begin)
            if self.id:
                query = query.exclude(pk=self.id)
            if query.count():
                raise ValidationError('Events already exists: , {}'.format(
                    '; '.join([str(v) for v in query])
                ))

    class Meta:
        ordering = ['begin']


class Client(CommonInfo, CommentMixin):
    """
    Client model
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    patronymic = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    phone = PhoneNumberField(max_length=30, db_index=True, unique=True)
    email = models.EmailField(max_length=200, db_index=True, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.patronymic)

    class Meta:
        ordering = ['last_name', 'first_name']
