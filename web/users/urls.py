# coding=utf-8
#!/usr/bin/python

from django.conf.urls import include, url
from django.contrib import admin
from users import views
from django.template import Context, Template
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^login/$', login, {"template_name": "login.html"}, name="login"),
    url(r'^logout/$', logout, {
        "template_name": "logged_out.html",
        "next_page": "/index",
    }, name="logout"),
    url(r'^register/$', views.register, name='register'),
    url(r'^account/$', views.account, name='account'),
    url(r'^([a-zA-Z0-9_]+)/$', views.index, name='userpage')
]
