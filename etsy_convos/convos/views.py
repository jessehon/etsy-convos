# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
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

    @detail_route(methods=['post'])
    def read(self, request, pk=None):
        message = self.get_object()
        message.set_is_read_for(request.user, True)
        message.save()
        serializer = self.serializer_class(instance=message, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def unread(self, request, pk=None):
        message = self.get_object()
        message.set_is_read_for(request.user, False)
        message.save()
        serializer = self.serializer_class(instance=message, context={'request': request})
        return Response(serializer.data)

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
