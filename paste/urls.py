from django.conf.urls import url
from django.views.static import serve
from paste import views
from webtools import settings


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^paste/(?P<slug>[A-z0-9]+)/(?P<renderer>[a-z]+)?$', views.show, name='paste'),
    url(r'^history$', views.history, name='history'),
    url(r'^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
]
