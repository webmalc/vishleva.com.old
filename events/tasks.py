from __future__ import absolute_import

from datetime import timedelta

import arrow
from django.conf import settings
from django.utils import timezone

from events.models import Event
from vishleva.celery import app
from vishleva.messengers.mailer import Mailer
from vishleva.messengers.sms.sender import Sender


@app.task
def event_notifications_task():
    events = Event.objects.get_for_notification()
    for event in events:
        Mailer.mail_managers(
            subject='Upcoming event' + ' - ' + event.title,
            template='emails/upcoming_event_manager.html',
            data={'event': event})
        client = event.client
        if client.email:
            Mailer.mail_user(
                subject='Напоминание о предстоящей фотосессии',
                template='emails/upcoming_event_client.html',
                data={'event': event},
                email=client.email)
        if client.phone:
            sender = Sender()
            begin = arrow.get(event.begin).to(settings.TIME_ZONE).datetime
            sender.send_sms(
                'Zdravstvuyte. Napominaju Vam, chto u Vas {} zaplanirovana fotosessija. Aleksandra Vishleva +7(903)735-60-96'.
                format(begin.strftime('%d.%m.%Y %H:%M')),
                client=client,
                send_before=begin - timedelta(hours=6))

        event.notified_at = timezone.now()
        event.save()


@app.task
def event_autoclose_task():
    events = Event.objects.get_for_closing()
    for event in events:
        event.status = 'closed'
        event.save()

    if events.count():
        Mailer.mail_managers(
            subject='Auto closed events',
            template='emails/closed_events_manager.html',
            data={'events': events}, )
