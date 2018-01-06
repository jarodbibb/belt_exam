from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^add_item/(?P<id>\d+)$', views.add_item),
    url(r'^suggest_item$', views.suggest),
    url(r'^create$', views.create),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^see_users/(?P<id>\d+)$', views.see_users),


]