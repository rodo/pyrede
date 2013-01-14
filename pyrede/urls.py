from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from pyrede.drp.views import PackageList
from pyrede.drp.views import PackageDetail
from pyrede.drp.models import Distribution
from pyrede.drp.models import DisPack


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',                       
                       url(r'^$', PackageList.as_view()),
                       url(r'^pypis/$', PackageList.as_view()),
                       url(r'^pypi/(?P<slug>.*)/$', PackageDetail.as_view()),
                       url(r'^distributions/$', ListView.as_view(model=Distribution)),
                       url(r'^packages/$', ListView.as_view(model=DisPack)),
                       url(r'^admin/', include(admin.site.urls)),
)
