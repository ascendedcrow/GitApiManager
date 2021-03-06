"""
Definition of urls for GitAPIManager.
"""
from datetime import datetime
from django.conf.urls import url,include
import django.contrib.auth.views

import app.forms
import app.views
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', app.views.home, name='home'),
    url(r'^issues/$', app.views.issues, name='issues'),
    url(r'^login/$',app.views.login,name='login'),
    url(r'^createissue/$', app.views.createissue, name='createissue'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
]
