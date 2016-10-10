from django.conf.urls import url, include
from django.contrib import admin
from pages.views import MainView, send_email
from django.views.i18n import javascript_catalog

js_info_dict = {
    'domain': 'django',
    'packages': ('pages', 'vishleva'),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^send_email$', send_email, name='send_email'),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
]

