__author__ = 'Code_Cola'

from django.conf.urls import include, url
from status import views

urlpatterns = [
    url(r'^ce/(\d+)/$', views.ce, name='ce_info'),
    url(r'^ce_json/(\d+)/$', views.ce_json, name='ce_info_json'),
    url(r'^code/(\d+)/$', views.show_code, name='show_code'),
    url(r'^get_status/(\d+)/$', views.get_status, name='get_status'),
    url(r'^get_problem_status/(\d+)/([a-zA-Z]+)/(\d+)/(\d+)/$', views.get_problem_status, name='get_problem_status'),
    url(r'^$', views.status, name='status')
]
