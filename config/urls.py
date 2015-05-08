# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from etsy_convos.convos.views import *
from rest_framework import routers, serializers, viewsets

# Comment the next two lines to disable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'messages', ConvoMessageViewSet)
router.register(r'threads', ConvoThreadViewSet)

urlpatterns = patterns('',  # noqa
    # Django Admin (Comment the next line to disable the admin)
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # Your stuff: custom urls includes go here


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
