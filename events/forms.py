from django import forms
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
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(), widget=forms.MultipleHiddenInput())
