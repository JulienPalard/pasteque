from django.conf.urls import patterns, url
from paste import views
from webtools import settings


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^paste/(?P<slug>[A-z0-9]+)/(?P<renderer>[a-z]+)?$', views.show, name='paste'),
    url(r'^history$', views.history, name='history'),
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
