from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^travels/addtrip$', views.addtrip),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/jointrip/(?P<trip_id>\d+)$', views.jointrip),
    url(r'^logout$', views.logout),
]
