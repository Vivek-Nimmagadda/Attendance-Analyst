from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register/$', views.register, name="register"),
    url(r'^about/$', views.register, name="about"),
    url(r'^(?P<lms_id>[A-Za-z0-9.]+)/update$', views.update_records, name="update"),
    url(r'^(?P<lms_id>[A-Za-z0-9.]+)/edit$', views.edit, name="edit"),
    url(r'^(?P<lms_id>[A-Za-z0-9.]+)/(?P<sem>[0-9]+)/$', views.get_records, name="records"),

]
