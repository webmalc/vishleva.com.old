from django.utils import translation
from django.conf import settings


class AdminLocaleMiddleware:

    @staticmethod
    def process_request(request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG
        else:
            request.LANG = settings.LANGUAGE_CODE
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG