import hashlib

from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse
from django.utils.timezone import now
from django.views import View

from mailing.models import Sms


class SmsApiView(View):
    def get(self, request):
        """ api - get sms list """
        key = self.request.GET.get('key')
        if not key or hashlib.md5(
                settings.API_KEY.encode('utf-8')).hexdigest() != key:
            return HttpResponseNotFound()

        sms = Sms.objects.filter(
            Q(send_before__gte=now()) | Q(send_before=None), send_at=None)[:30]
        for entry in sms:
            entry.send_at = now()
            entry.save()
        return JsonResponse(
            serializers.serialize('json', sms, fields={'text', 'phone'}),
            safe=False)
