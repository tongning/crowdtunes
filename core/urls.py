from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download/(?P<filename>\w+)$', views.download, name='download'),
    url(r'^downloadSong/(?P<filename>\w+)$', views.downloadSong, name='downloadSong'),
    url(r'^combined/$', views.combined, name='combined'),
    url(r'^about/$', views.about, name='about'),
    url(r'^createYourOwn/$', views.createYourOwn, name='create')

]

