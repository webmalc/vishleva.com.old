from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Client


@receiver(pre_save, sender=Client, dispatch_uid="events_client_pre_save")
def events_client_pre_save(sender, **kwargs):
    """
    Client pre save
    :param sender: Client
    :param kwargs: dict
    :return:
    """
    pass

