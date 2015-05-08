# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .models import *
from .serializers import *

class ConvoViewSet(viewsets.ModelViewSet):
    queryset = Convo.objects.all()
    serializer_class = ConvoSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoPreviewSerializer
        return super(ConvoViewSet, self).list(self, request, *args, **kwargs)

class ConvoThreadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConvoThread.objects.all()
    serializer_class = ConvoThreadSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoThreadPreviewSerializer
        return super(ConvoThreadViewSet, self).list(self, request, *args, **kwargs)
