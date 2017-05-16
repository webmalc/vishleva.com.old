from __future__ import absolute_import

from mailing.models import Sms
from vishleva.celery import app
from vishleva.messengers.mailer import Mailer


@app.task
def new_sms_notifications_task():
    sms = Sms.objects.get_for_send()
    if sms.count():
        Mailer.mail_managers(
            subject='New sms waiting',
            template='emails/new_sms_manager.html',
            data={'sms': sms})
