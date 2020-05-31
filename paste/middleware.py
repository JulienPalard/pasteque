from webtools import settings


from django.contrib.sessions.middleware import (
    SessionMiddleware as DjangoSessionMiddleware,
)


class SessionMiddleware(DjangoSessionMiddleware):
    def process_request(self, request):
        if "admin" in request.path:
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
            request.session = self.SessionStore(session_key)
        else:
            request.session = {}

    def process_response(self, request, response):
        if "admin" in request.path:
            return super().process_response(request, response)
        else:
            return response
