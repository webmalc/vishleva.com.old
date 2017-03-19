from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from vishleva.models import CommonInfo


class Sms(CommonInfo):
    """ Sms entry class """

    @classmethod
    def create(cls, phone, text):
        """ create new sms """
        sms = cls(phone=phone, text=text)
        return sms

    phone = PhoneNumberField(max_length=30, db_index=True)
    text = models.TextField(max_length=255, db_index=True)
    send_at = models.DateTimeField(db_index=True, null=True)

    class Meta:
        verbose_name_plural = 'Sms'
