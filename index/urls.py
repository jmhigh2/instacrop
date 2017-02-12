from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$', views.index, name="index"),
    url(r'^google$', views.link_google, name="google"),
    url(r'^auth$', views.google_auth, name = 'google_auth'),
    url(r'^create$', views.create_contact, name="create"),
    url(r'^update$', views.update_contact, name="update"),
]
