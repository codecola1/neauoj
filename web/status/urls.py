__author__ = 'Code_Cola'

from django.conf.urls import include, url
from status import views


urlpatterns = [
    url(r'^ce/(\d+)/$', views.ce, name = 'ce_info'),
    url(r'^$', views.status, name = 'status')
]