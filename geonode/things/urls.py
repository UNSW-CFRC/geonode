from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^myair:(?P<id>[^/]+)/view$', views.myair_view, name='myair_view'),
    url(r'^myair:(?P<id>[^/]+)/latest$', views.myair_latest, name='myair_latest'),
    url(r'^myair:(?P<id>[^/]+)/dashboard$', views.myair_dashboard, name='myair_dashboard'),
]
