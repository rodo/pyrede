from django.conf.urls import patterns, include, url
from pyrede.drp.views import PackageList

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',                       
                       url(r'^$', PackageList.as_view()),
                       url(r'^packages/$', PackageList.as_view()),
)
