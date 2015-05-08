# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ConvoThread, Convo

admin.site.register(ConvoThread)
admin.site.register(Convo)
