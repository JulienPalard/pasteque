from django.conf.urls import url
from django.views.static import serve
from paste import views
from webtools import settings


urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^history$", views.history, name="history"),
    url(r"^static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
    url(
        r"^paste/(?P<slug>[a-zA-Z0-9]+)/(?P<renderer>[a-z]+)?$",
        views.show,
        name="paste",
    ),
    url(r"^(?P<slug>[0-9][a-zA-Z0-9]+)$", views.show, name="short_paste"),
]
