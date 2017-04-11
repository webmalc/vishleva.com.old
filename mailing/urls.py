from django.conf.urls import url

from mailing.views import SmsApiView

urlpatterns = [
    url(r'^sms/list', SmsApiView.as_view(), name='sms_api_list'),
]
