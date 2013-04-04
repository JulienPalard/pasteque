from django.conf import settings


def app_details(request):
    """Passes settings details to the templates."""
    return {'APP_NAME': settings.APP_NAME,
            'APP_VERSION': settings.APP_VERSION,
            'DISPLAY_NAME': settings.DISPLAY_NAME}
