# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *

class BaseConvoMessageSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = ConvoMessage

    def get_is_read(self, obj):
        return obj.get_is_read_for(self.context['request'].user)

class ConvoMessageSerializer(BaseConvoMessageSerializer):
    subject = serializers.CharField(source='thread.subject')

    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'subject', 'body', 'is_read',)
        read_only_fields = ('sender',)

    def create(self, validated_data):
        thread_data = validated_data.get('thread', None)
        thread = ConvoThread.objects.create(**thread_data)
        validated_data['thread'] = thread
        return ConvoMessage.objects.create(**validated_data)

class ConvoMessageNestedSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body', 'is_read',)
        read_only_fields = ('sender', 'recipient',)

class ConvoMessageNestedPreviewSerializer(BaseConvoMessageSerializer):
    class Meta(BaseConvoMessageSerializer.Meta):
        fields = ('id', 'sender', 'recipient', 'body_excerpt', 'is_read',)

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
