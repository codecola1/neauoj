__author__ = 'Code_Cola'

from django.conf.urls import include, url
from status import views


urlpatterns = [
    url(r'^ce/(\d+)/$', views.ce, name = 'ce_info'),
    url(r'^code/(\d+)/$', views.show_code, name = 'show_code'),
    url(r'^get_status/(\d+)/$', views.get_status, name = 'get_status'),
    url(r'^$', views.status, name = 'status')
]