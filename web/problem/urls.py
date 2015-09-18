__author__ = 'Code_Cola'

from django.conf.urls import include, url
from problem import views


urlpatterns = [
    url(r'^p/([0-9]+)$', views.problem_main, name = 'problempage'),
    url(r'info/(\w+)/([0-9]+)$', views.get_problem_info, name = 'get_problem_info'),
    url(r'acmlist$', views.problem_list, name = 'problem_acmlist'),
    url(r'studentlist$', views.problem_list, name = 'problem_studentlist'),
    url(r'vjudgelist$', views.problem_list, name = 'problem_vjudgelist'),
]