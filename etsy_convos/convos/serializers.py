# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *

class BaseConvoMessageSerializer(serializers.ModelSerializer):
    read_at = serializers.SerializerMethodField()

    class Meta:
        model = ConvoMessage

    def get_read_at(self, obj):
        return obj.get_read_at_for(self.context['request'].user)

class ConvoMessageSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body', 'read_at',)

class ConvoMessagePreviewSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body_excerpt', 'read_at',)

class BaseConvoThreadSerializer(serializers.ModelSerializer):
    messages = ConvoMessagePreviewSerializer(source='convomessages', many=True)
    last_message = ConvoMessagePreviewSerializer(source='get_last_message')

    class Meta:
        model = ConvoThread

class ConvoThreadSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'messages')

class ConvoThreadPreviewSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'last_message')
