# -*- coding: utf-8 -*-
from rest_framework import filters

class ActiveForUserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.active_for(request.user)

class ThreadFolderFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        folder = request.QUERY_PARAMS.get('folder', None)
        if folder is not None:
            queryset = queryset.folder_for(folder, request.user)
        return queryset
