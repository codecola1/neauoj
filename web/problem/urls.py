__author__ = 'Code_Cola'

from django.conf.urls import include, url
from problem import views


urlpatterns = [
    url(r'^p/([0-9]+)$', views.problem_main, name = 'problempage'),
]