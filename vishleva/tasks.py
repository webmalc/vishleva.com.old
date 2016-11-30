from __future__ import absolute_import
from vishleva.celery import app
from vishleva.messengers.mailer import Mailer


@app.task
def mail_managers_task(subject, template, data):
    """
    Mail to site managers
    :param subject: subject string
    :param template: template name
    :param data: data dict for template rendering
    :return: None
    """
    Mailer.mail_managers(subject=subject, template=template, data=data)