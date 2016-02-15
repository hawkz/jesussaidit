from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from jesussaidit.quotes.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jesussaidit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<book>[-\w]+)/(?P<chapter>\d+)/(?P<verse>\d+)/$', quote_view, name='quote-view'),
    url(r'^(?P<book>[-\w]+)/(?P<chapter>\d+)/$', chapter_view, name='chapter-view'),
    url(r'^$', AllQuotesView.as_view(), name='quote-list'),
    url(r'^search/$', search, name='search'),
)

# Serving static/media under debug
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
