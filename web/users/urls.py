#coding=utf-8
#!/usr/bin/python

from django.conf.urls import include, url
from django.contrib import admin
from users import views

urlpatterns = [
	url(r'^$', views.test, name = 'test'),
]
