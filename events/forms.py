from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _

from events.models import Client


class SmsForm(forms.Form):
    """
    Admin sms form
    """
    message = forms.CharField(
        label=_('message'),
        validators=[MaxLengthValidator(140)],
        widget=forms.Textarea(attrs={'placeholder': _('message text')}))
    send_before = forms.SplitDateTimeField(
        required=False, widget=AdminSplitDateTime())
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(), widget=forms.MultipleHiddenInput())
