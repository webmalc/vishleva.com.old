from django.http import JsonResponse
from django.views import View


class SmsApiView(View):
    def get(self, request):
        """ api - get sms list """
        return JsonResponse({'1233': 1233, 'erwer': '1233'}, safe=False)
