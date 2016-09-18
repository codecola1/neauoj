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
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^signing/$', views.signing, name='signing'),
    url(r'^accept/([0-9]+)/$', views.accept, name='accept'),
    url(r'^reject/([0-9]+)/$', views.reject, name='reject'),
    url(r'^userpage/([a-zA-Z0-9_]+)/$', views.index, name='userpage'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^edit_information/$', views.edit_information, name='edit_information'),
    url(r'^add_account/$', views.add_account, name='add_account'),
    url(r'^judge_account/$', views.judge_account, name='judge_account'),
    url(r'^updating/([a-zA-Z0-9_]+)/$', views.updating, name='updating'),
    url(r'^permission/$', views.permission, name='permission'),
    url(r'^useradmin/$', views.useradmin, name='useradmin'),
    url(r'^clone_contest/$', views.clone_contest, name='clone_contest'),
]
