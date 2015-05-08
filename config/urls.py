# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Comment the next two lines to disable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',  # noqa
    # Django Admin (Comment the next line to disable the admin)
    url(r'^admin/', include(admin.site.urls)),

    # Your stuff: custom urls includes go here


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
