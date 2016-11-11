from django.conf.urls import url, include
from django.contrib import admin
from photologue.views import PhotoDetailView
from django.views.i18n import javascript_catalog
from django.conf import settings
from django.conf.urls.static import static
from pages.views import MainView, send_email, GalleryView

js_info_dict = {
    'domain': 'django',
    'packages': ('pages', 'vishleva'),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'^pages/', include('pages.urls', namespace='pages')),
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^send_email$', send_email, name='send_email'),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),

    # photologue
    url(r'^photo/', include(
        [
            url(r'^gallery/(?P<slug>[\-\d\w]+)(?:/(?P<page>\d+))?/$', GalleryView.as_view(), name='pl-gallery'),
            url(r'^photo/(?P<slug>[\-\d\w]+)/$', PhotoDetailView.as_view(), name='pl-photo'),
         ],
        namespace='photologue'
    )),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
