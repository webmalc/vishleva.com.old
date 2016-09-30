from django.conf.urls import url, include
from django.contrib import admin
from pages.views import MainView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'^$', MainView.as_view(), name='index'),
]

