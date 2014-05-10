from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jesussaidit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^chapter/(?P<pk>\d+)/$', ChapterView.as_view(), name='chapter-view'),
    url(r'^(?P<slug>[-\w]+)/$', QuoteView.as_view(), name='quote-view'),
    url(r'^$', AllQuotesView.as_view(), name='quote-list'),
)

# Serving static/media under debug
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
