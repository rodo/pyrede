from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from pyrede.drp.views import PackageList
from pyrede.drp.views import ObsoleteList
from pyrede.drp.views import PackageDetail
from pyrede.drp.views import DistributionDetail
from pyrede.drp.views import DistributionPackages
from pyrede.drp.models import Distribution
from pyrede.drp.models import DisPack
from pyrede.drp.models import DebianITP
from pyrede.drp.models import Lookup
from tastypie.api import Api
from pyrede.drp.api import PackageResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Implement API version 1                                                                                
v1_api = Api(api_name='v1')
# Register Shows                                                                                         
v1_api.register(PackageResource())

urlpatterns = patterns('',                       
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^accounts/profile/$', 'pyrede.drp.views.profile'),
                       url(r'^$', 'pyrede.drp.views.userreq'),
                       url(r'^analyze/(?P<pk>\d+)/$', 'pyrede.drp.views.analyze'),
                       url(r'^analyze/(?P<pk>\d+)/(?P<dist>\d+)/requirements.txt$', 'pyrede.drp.views.analyzereq'),
                       url(r'^analyze/$', 'pyrede.drp.views.analyze'),
                       url(r'^analyzes/$', ListView.as_view(model=Lookup,paginate_by=17)),
                       url(r'^pypis/latest/$', PackageList.as_view()),
                       url(r'^pypis/$', PackageList.as_view()),
                       url(r'^json/pypi/(?P<slug>.*)/$', 'pyrede.drp.views.jsonpypi'),
                       url(r'^add/pypi/(?P<slug>.*)/$', 'pyrede.drp.views.adddispack'),
                       url(r'^update/dispack/(?P<pk>\d+)/(?P<new_version>.*)$', 'pyrede.drp.views.updispack'),
                       url(r'^pypi/(?P<slug>.*)/sub/$', 'pyrede.drp.views.subscribe'),
                       url(r'^pypi/(?P<slug>.*)/unsub/(?P<uuid>.*)/$', 'pyrede.drp.views.unsubscribe'),
                       url(r'^pypi/(?P<slug>.*)/$', PackageDetail.as_view()),
                       url(r'^distributions/$', ListView.as_view(model=Distribution)),
                       url(r'^distribution/(?P<pk>\d+)/packages/$', DistributionPackages.as_view()),
                       url(r'^distribution/(?P<pk>\d+)/$', DistributionDetail.as_view()),
                       url(r'^packages/$', ListView.as_view(model=DisPack,paginate_by=17)),
                       url(r'^obsolete/$', ObsoleteList.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^search/', include('haystack.urls')),
                       url(r'^about/$', 'pyrede.drp.views.about'),
                       url(r'^robots.txt$', 'pyrede.drp.views.robots'),
                       url(r'^itps/$', ListView.as_view(model=DebianITP)),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^captcha/', include('captcha.urls')),

)


