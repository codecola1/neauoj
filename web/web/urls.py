"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from web import settings
import os

urlpatterns = [
    url(r'^$', 'core.views.index', name='home'),
    url(r'^index/$', 'core.views.index', name='home'),
    url(r'^test/$', 'core.views.test'),
    url(r'^submit/$', 'status.views.submit', name='submit'),
    url(r'status/', include('status.urls')),
    url(r'^accounts/', include('users.urls')),
    url(r'^problem/', include('problem.urls')),
]

urlpatterns += patterns('',
                        (r'^img/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': os.path.join(settings.STATIC_PATH, 'img')} ),

                        (r'^upload/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': os.path.join(settings.STATIC_PATH, 'upload')} ),

                        (r'^css/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': os.path.join(settings.STATIC_PATH, 'css')} ),

                        (r'^js/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': os.path.join(settings.STATIC_PATH, 'js')} ),
)