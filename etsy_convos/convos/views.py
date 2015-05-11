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

    def perform_create(self, serializer):
        sender = self.request.user
        serializer.save(sender=sender)

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
        viewsets.GenericViewSet):
    queryset = ConvoMessage.objects.all()
    serializer_class = ConvoMessageNestedSerializer

    def get_parent_thread_object(self):
        thread_query_dict = self.get_parents_query_dict()
        thread_id = thread_query_dict['thread']
        thread = ConvoThread.objects.get(id=thread_id)
        return thread

    def perform_create(self, serializer):
        thread = self.get_parent_thread_object()
        sender = self.request.user
        participants = thread.get_participants()
        recipient = participants.exclude(pk=sender.pk).first()
        serializer.save(thread=thread, sender=sender, recipient=recipient)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoMessageNestedPreviewSerializer
        return super(ConvoMessageNestedViewSet, self).list(self, request, *args, **kwargs)

class ConvoThreadViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ConvoThread.objects.all()
    serializer_class = ConvoThreadSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ConvoThreadPreviewSerializer
        return super(ConvoThreadViewSet, self).list(self, request, *args, **kwargs)
