# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *

class BaseConvoSerializer(serializers.ModelSerializer):
    read_at = serializers.SerializerMethodField()

    class Meta:
        model = Convo

    def get_read_at(self, obj):
        return obj.get_read_at_for(self.context['request'].user)

class ConvoSerializer(BaseConvoSerializer):
    class Meta(BaseConvoSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body', 'read_at',)

class ConvoPreviewSerializer(BaseConvoSerializer):
    class Meta(BaseConvoSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body_excerpt', 'read_at',)

class BaseConvoThreadSerializer(serializers.ModelSerializer):
    convos = ConvoPreviewSerializer(source='convo_set', many=True)
    last_convo = ConvoPreviewSerializer(source='get_last_convo')

    class Meta:
        model = ConvoThread

class ConvoThreadSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'convos')

class ConvoThreadPreviewSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'last_convo')
