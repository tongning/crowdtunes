from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download/(?P<filename>\w+)$', views.download, name='download'),
    url(r'^/combined/$', views.combined, name='combined')

]