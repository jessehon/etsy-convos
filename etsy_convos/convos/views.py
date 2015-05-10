# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import *
from .serializers import *

class ConvoMessageViewSet(NestedViewSetMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = ConvoMessage.objects.all()
    serializer_class = ConvoMessageSerializer

class ConvoMessageNestedViewSet(NestedViewSetMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = ConvoMessage.objects.all()
    serializer_class = ConvoMessageNestedSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoMessageNestedPreviewSerializer
        return super(ConvoMessageNestedViewSet, self).list(self, request, *args, **kwargs)

class ConvoThreadViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ConvoThread.objects.all()
    serializer_class = ConvoThreadSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoThreadPreviewSerializer
        return super(ConvoThreadViewSet, self).list(self, request, *args, **kwargs)
