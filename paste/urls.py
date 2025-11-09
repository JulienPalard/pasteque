from django.urls import path
from django.views.static import serve

from paste import views
from webtools import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("history", views.history, name="history"),
    path("static/<slug:path>", serve, {"document_root": settings.STATIC_ROOT}),
    path(
        "paste/<slug:slug>/<slug:renderer>",
        views.show,
        name="paste",
    ),
    path(
        "paste/<slug:slug>/",
        views.show,
        name="paste",
    ),
    path("<slug:slug>", views.show, name="short_paste"),
]
