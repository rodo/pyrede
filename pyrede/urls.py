from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from pyrede.drp.views import PackageList
from pyrede.drp.views import PackageDetail
from pyrede.drp.models import Distribution
from pyrede.drp.models import DisPack
from pyrede.drp.models import Lookup


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',                       
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^accounts/profile/$', 'pyrede.drp.views.profile'),
                       url(r'^$', 'pyrede.drp.views.userreq'),
                       url(r'^analyze/(?P<pk>\d+)/$', 'pyrede.drp.views.analyze'),
                       url(r'^analyze/(?P<pk>\d+)/(?P<dist>\d+)/requirements.txt$', 'pyrede.drp.views.analyzereq'),
                       url(r'^analyze/$', 'pyrede.drp.views.analyze'),
                       url(r'^analyzes/$', ListView.as_view(model=Lookup,paginate_by=17)),
                       url(r'^pypis/$', PackageList.as_view()),
                       url(r'^json/pypi/(?P<slug>.*)/$', 'pyrede.drp.views.jsonpypi'),
                       url(r'^add/pypi/(?P<slug>.*)/$', 'pyrede.drp.views.adddispack'),
                       url(r'^pypi/(?P<slug>.*)/add/$', 'pyrede.drp.views.adddispack'),
                       url(r'^pypi/(?P<slug>.*)/sub/$', 'pyrede.drp.views.subscribe'),
                       url(r'^pypi/(?P<slug>.*)/unsub/(?P<uuid>.*)/$', 'pyrede.drp.views.unsubscribe'),
                       url(r'^pypi/(?P<slug>.*)/$', PackageDetail.as_view()),
                       url(r'^distributions/$', ListView.as_view(model=Distribution)),
                       url(r'^distribution/(?P<pk>\d+)/$', DetailView.as_view(model=Distribution)),
                       url(r'^packages/$', ListView.as_view(model=DisPack,paginate_by=17)),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^search/', include('haystack.urls')),
                       url(r'^about/$', 'pyrede.drp.views.about'),
)
