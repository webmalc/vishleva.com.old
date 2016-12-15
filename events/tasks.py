from __future__ import absolute_import
from vishleva.celery import app
from events.models import Event
from django.utils import timezone
from vishleva.messengers.mailer import Mailer


@app.task
def event_notifications_task():
    events = Event.objects.get_for_notification()
    for event in events:
        Mailer.mail_managers(
            subject='Upcoming event' + ' - ' + event.title,
            template='emails/upcoming_event_manager.html',
            data={'event': event}
        )
        client = event.client
        if client.email:
            Mailer.mail_user(
                subject='Напоминание о предстоящей фотосессии',
                template='emails/upcoming_event_client.html',
                data={'event': event},
                email=client.email
            )
        event.notified_at = timezone.now()
        event.save()
