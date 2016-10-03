from django.conf.urls import url, include
from django.contrib import admin
from pages.views import MainView, send_email

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^send_email$', send_email, name='send_email')
]

