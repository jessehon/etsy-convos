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
    subject = serializers.CharField(source='thread.subject')

    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'subject', 'body', 'read_at',)

    def create(self, validated_data):
        thread_data = validated_data.get('thread', None)
        thread = ConvoThread.objects.create(**thread_data)
        validated_data['thread'] = thread
        return ConvoMessage.objects.create(**validated_data)

class ConvoMessageNestedSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body', 'read_at',)

class ConvoMessageNestedPreviewSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body_excerpt', 'read_at',)

class BaseConvoThreadSerializer(serializers.ModelSerializer):
    messages = ConvoMessageNestedPreviewSerializer(source='convomessages', many=True)
    last_message = ConvoMessageNestedPreviewSerializer(source='get_last_message')

    class Meta:
        model = ConvoThread

class ConvoThreadSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'messages')
        read_only_fields = ('messages')

class ConvoThreadPreviewSerializer(BaseConvoThreadSerializer):
    class Meta(BaseConvoThreadSerializer.Meta):
        fields = ('id', 'subject', 'last_message')
