__author__ = 'Code_Cola'

from django.conf.urls import include, url
from status import views


urlpatterns = [
    url(r'^submit$', views.submit, name = 'submit'),
]