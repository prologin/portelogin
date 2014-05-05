from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pasteur_gate/$', 'digicode.views.open_pasteur_gate'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
