from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^leagues', views.leagues_test, name='leagues_test'),
    url(r'^test', views.test, name='test'),
    url(r'^mapping', views.mapping, name='mapping'),
]
