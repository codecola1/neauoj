__author__ = 'Code_Cola'

from django.conf.urls import include, url
from contest import views

urlpatterns = [
    url(r'acmlist$', views.contest_list, name='contest_acmlist'),
    url(r'studentlist$', views.contest_list, name='contest_studentlist'),
    url(r'vjudgelist$', views.contest_list, name='contest_vjudgelist'),
    url(r'info/(\w+)/([0-9]+)$', views.get_contest_info, name='get_contest_info'),
    url(r'c/([0-9]+)$', views.contest_main, name='contest_main'),
    url(r'problem/([0-9]+)/([0-9]+)$', views.get_problem, name='get_contest_problem'),
    url(r'status/([0-9]+)/([0-9]+)$', views.get_status, name='get_contest_status'),
    url(r'info/([0-9]+)$', views.get_some_info, name='get_some_info'),
    url(r'rank/([0-9]+)$', views.get_rank, name='get_rank'),
    url(r'code/(\d+)/(\d+)/$', views.get_code, name='get_code'),
    url(r'add/(\w+)/$', views.add_contest, name='add_contest'),
    url(r'hide/$', views.hide_contest, name='hide_contest'),
    url(r'show/$', views.show_contest, name='show_contest'),
]
