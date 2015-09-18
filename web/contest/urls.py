__author__ = 'Code_Cola'

from django.conf.urls import include, url
from contest import views


urlpatterns = [
    url(r'acmlist$', views.contest_list, name = 'contest_acmlist'),
    url(r'studentlist$', views.contest_list, name = 'contest_studentlist'),
    url(r'vjudgelist$', views.contest_list, name = 'contest_vjudgelist'),
]