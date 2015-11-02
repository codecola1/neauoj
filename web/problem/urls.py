__author__ = 'Code_Cola'

from django.conf.urls import include, url
from problem import views


urlpatterns = [
    url(r'^p/([0-9]+)$', views.problem_main, name = 'problempage'),
    url(r'list/(\w+)/([0-9]+)$', views.get_problem_list, name = 'get_problem_list'),
    url(r'info/(\w+)/([0-9]+)/([0-9]+)$', views.get_problem_info, name = 'get_problem_info'),
    url(r'add_problem/', views.add_problem, name='add_problem'),
    url(r'acmlist$', views.problem_list, name = 'problem_acmlist'),
    url(r'studentlist$', views.problem_list, name = 'problem_studentlist'),
    url(r'vjudgelist$', views.problem_list, name = 'problem_vjudgelist'),
]